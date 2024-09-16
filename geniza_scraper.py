import argparse
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://geniza.princeton.edu/en/documents/"
SEARCH_URL = "https://geniza.princeton.edu/en/documents/?q=&docdate_0=&docdate_1=&sort=docdate_desc&page="

class Folio(BaseModel):
    folio_name: Optional[str] = None
    folio_lines_original: Optional[List[str]] = None
    folio_lines_translation: Optional[List[str]] = None
    original_language: Optional[str] = None
    translation_language: Optional[str] = None

class TextData(BaseModel):
    folios: List[Folio]
    transcriber: Optional[str] = None

class GenizaDocument(BaseModel):
    pgpid: int
    primary_languages: Optional[List[str]] = None
    secondary_languages: Optional[List[str]] = None
    editor: Optional[str] = None
    description: Optional[str] = None
    text_datas: Optional[List[TextData]] = None

def get_languages(soup: BeautifulSoup, language_type: str) -> List[str]:
    language_type = language_type.lower()
    if language_type not in ['primary', 'secondary']:
        raise ValueError("Invalid language type. Choose 'Primary' or 'Secondary'.")

    search_terms = {
        'primary': ['Primary Language', 'Primary Languages'],
        'secondary': ['Secondary Language', 'Secondary Languages']
    }

    metadata_section = soup.find('dl', class_='metadata-list secondary')
    if not metadata_section:
        return []

    languages = []
    for dt in metadata_section.find_all('dt'):
        if any(term in dt.text for term in search_terms[language_type]):
            languages.extend(dd.text.strip() for dd in dt.find_next_siblings('dd'))

    return languages

def extract_text_content(div: BeautifulSoup) -> Dict[str, Optional[str]]:
    return {
        "key": next((cls for cls in div['class'] if cls.startswith(('ed-', 'tr-'))), None),
        "header": div.find('h3').text.strip() if div.find('h3') else "No header",
        "text": [item.text.strip() for item in div.select('li, p')],
        "data_label": div.get('data-label'),
        "lang": div.get('lang')
    }

def extract_content(soup: BeautifulSoup, content_type: str) -> Dict[str, Dict[str, Any]]:
    content = {}
    for div in soup.find_all('div', class_=lambda x: x and content_type in x):
        data = extract_text_content(div)
        if data["text"]:
            content[data["header"]] = {
                content_type: data["key"],
                "text": data["text"],
                "data_label": data["data_label"],
                "lang": data["lang"]
            }
    return content

def parse_geniza_document(soup: BeautifulSoup) -> GenizaDocument:
    pgpid = int(soup.find('link', rel='canonical')['href'].split('/')[-2])
    primary_languages = get_languages(soup, 'primary')
    secondary_languages = get_languages(soup, 'secondary')
    editors = [ed.text.strip() for ed in soup.find_all('dd') if ed.find_previous_sibling('dt') and ed.find_previous_sibling('dt').text.strip() == 'Editor']
    description = soup.find('section', class_='description').p.text.strip()
    
    transcriptions = extract_content(soup, 'transcription')
    translations = extract_content(soup, 'translation')
    
    text_datas = []
    for header in transcriptions.keys():
        folios = []
        for i, (orig, trans) in enumerate(zip(transcriptions[header]['text'], translations.get(header, {}).get('text', []))):
            folios.append(Folio(
                folio_name=f"Folio {i+1}",
                folio_lines_original=[orig],
                folio_lines_translation=[trans] if trans else None,
                original_language=transcriptions[header]['lang'],
                translation_language=translations.get(header, {}).get('lang')
            ))
        text_datas.append(TextData(folios=folios, transcriber=editors[0] if editors else None))

    return GenizaDocument(
        pgpid=pgpid,
        primary_languages=primary_languages,
        secondary_languages=secondary_languages,
        editor=', '.join(editors),
        description=description,
        text_datas=text_datas
    )

def fetch_document_ids(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    document_links = soup.select('a[href^="/en/documents/"]')
    return [link['href'].split('/')[-2] for link in document_links if link['href'].split('/')[-2].isdigit()]

def process_document(pgpid):
    url = f"{BASE_URL}{pgpid}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        document = parse_geniza_document(soup)
        logger.info(f"Successfully parsed document with PGPID: {document.pgpid}")
        return document
    except requests.RequestException as e:
        logger.error(f"Error fetching document {pgpid}: {str(e)}")
    except Exception as e:
        logger.error(f"Error parsing document {pgpid}: {str(e)}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Scrape Geniza documents")
    parser.add_argument("--pgpid", type=int, help="PGPID of the document to scrape")
    parser.add_argument("--all", action="store_true", help="Scrape all documents")
    parser.add_argument("--transcriptions", action="store_true", help="Include documents with transcriptions")
    parser.add_argument("--translations", action="store_true", help="Include documents with translations")
    args = parser.parse_args()

    if args.all:
        if not (args.transcriptions or args.translations):
            parser.error("When using --all, specify --transcriptions and/or --translations")
        
        search_params = []
        if args.transcriptions:
            search_params.append("has_transcription=on")
        if args.translations:
            search_params.append("has_translation=on")
        
        search_url = SEARCH_URL + "&".join(search_params) + "&"
        
        page = 1
        while True:
            url = f"{search_url}page={page}"
            document_ids = fetch_document_ids(url)
            if not document_ids:
                break
            for doc_id in document_ids:
                process_document(doc_id)
            page += 1
    elif args.pgpid:
        process_document(args.pgpid)
    else:
        parser.error("Either --pgpid or --all must be specified")

if __name__ == "__main__":
    main()