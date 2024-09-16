from typing import List, Dict, Optional
from bs4 import BeautifulSoup
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

def get_languages(soup, language_type):
    """
    Extracts primary or secondary languages from the provided BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the HTML content.
    language_type (str): The type of languages to extract. Accepts 'Primary' or 'Secondary'.

    Returns:
    list: A list of extracted languages. Returns an empty list if none are found.
    """
    # Validate the input language_type
    language_type = language_type.lower()
    if language_type not in ['primary', 'secondary']:
        raise ValueError("Invalid language type. Choose 'Primary' or 'Secondary'.")

    # Define the search terms based on the language type
    search_terms = {
        'primary': ['Primary Language', 'Primary Languages'],
        'secondary': ['Secondary Language', 'Secondary Languages']
    }

    # Find the metadata section
    metadata_section = soup.find('dl', class_='metadata-list secondary')
    
    # Return an empty list if the metadata section is not found
    if not metadata_section:
        return []

    # Extract the languages based on the search terms
    languages = []
    for dt in metadata_section.find_all('dt'):
        if any(term in dt.text for term in search_terms[language_type]):
            languages.extend(dd.text.strip() for dd in dt.find_next_siblings('dd'))

    return languages


def extract_transcriptions(soup):
    transcriptions = {}
    for div in soup.find_all('div', class_=lambda x: x and 'transcription' in x):
        key = next((cls for cls in div['class'] if cls.startswith('ed-')), None)
        if key:
            header = div.find('h3').text.strip() if div.find('h3') else None
            text = [item.text.strip() for item in div.select('li, p')]
            data_label = div.get('data-label')
            
            lang = div.get('lang')
            if header is None and len(text) != 0:
                header = "they didn't give this a header"
            if header:
                transcriptions[header] = {
                    "transcription": key,
                    "text": text,
                    'data_label': data_label,
                    'lang': lang
                }

    return transcriptions

def extract_translations(soup):
    translations = {}

    for div in soup.find_all('div', class_=lambda x: x and 'translation' in x):
        key = next((cls for cls in div['class'] if cls.startswith('tr-')), None)
        if key:
            header = div.find('h3').text.strip() if div.find('h3') else None
            text = [item.text.strip() for item in div.select('li, p')]
            data_label = div.get('data-label')
            lang = div.get('lang')
            if header is None and len(text) != 0:
                header = "they didn't give this a header"
            if header:
                translations[header] = {
                    "translation": key,
                    "text": text,
                    'data_label': data_label,
                    'lang': lang
                }

    return translations


#Try to get to work eventually
def merge_folios(transcriptions, translations, threshold=80):
    folios = []
    for trans_header in transcriptions.keys():
        # Find the best match in translations using fuzzy matching
        match, score = process.extractOne(trans_header, translations.keys(), scorer=fuzz.ratio)
        folio_entry = {
            "folio": trans_header,
            "transcription": transcriptions[trans_header]
        }
        # Add translation if the match score is above the threshold
        if score >= threshold:
            folio_entry["translation"] = translations[match]
        folios.append(folio_entry)
    return folios


def parse_geniza_document(soup):
    

    # Extract basic information
    pgpid = int(soup.find('link', rel='canonical')['href'].split('/')[-2])
    
    # Extract primary and secondary languages
    #Works
    primary_languages = get_languages(soup, 'primary')
    secondary_languages = get_languages(soup, 'secondary')
    


    editors = [ed.text.strip() for ed in soup.find_all('dd') if ed.find_previous_sibling('dt') and ed.find_previous_sibling('dt').text.strip() == 'Editor']
    description = soup.find('section', class_='description').p.text.strip()

    # Extract transcriptions and translations
    translations = extract_translations(soup)
    transcriptions = extract_transcriptions(soup)


    # Create and return the GenizaDocument object
    return {
        "pgpid":pgpid,
        "primary_languages" :primary_languages,
        "secondary_languages" :secondary_languages,
        "editor" :', '.join(editors),
        "description" :description,
        "transcriptions" :transcriptions,
        "translations" :translations
    }

# Usage
if __name__ == "__main__":
    html_content = open("geniza_3556.html", "r")

    soup = BeautifulSoup(html_content, 'html.parser')
    print(parse_geniza_document(soup))
    #trans = extract_transcriptions_and_translations(soup)
