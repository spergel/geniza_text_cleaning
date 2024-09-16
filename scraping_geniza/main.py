import requests
import utils
import future
from bs4 import BeautifulSoup
import re
import json

base_url = "https://geniza.princeton.edu/en/documents/?q=&docdate_0=&docdate_1=&has_transcription=on&sort=docdate_desc&page="
urls = [f"{base_url}{n}" for n in range(1, 121)]

pattern = re.compile(r'^/en/documents/\d+/$')

session = requests.Session()

all_links = []
docs = []

for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all <a> tags with href attributes
        links = soup.find_all('a', href=pattern)
        for link in links:
            href = link.get('href')
            
            if href:
                all_links.append(href)
                response_2 = requests.get(f'https://geniza.princeton.edu{href}')
                soup_2 = BeautifulSoup(response_2.content, 'html.parser')
                doc = utils.parse_geniza_document(soup_2)
                docs.append(doc)
                print(doc)
    else:
        print(f"Failed to fetch {url} with status code {response.status_code}")

with open('geniza_documents.json', 'w', encoding='utf-8') as f:
    json.dump(docs, f, ensure_ascii=False, indent=4)