from typing import List, Optional, Tuple
from pydantic import BaseModel
from models import Folio, TextData
from bs4 import BeautifulSoup

html_content = open("geniza_3556.html", "r")

soup = BeautifulSoup(html_content, 'html.parser')


# transcriptions = {}
# translations = {}

# # Collect transcriptions
# for div in soup.find_all('div', class_=lambda x: x and 'transcription' in x):
#     key = next((cls for cls in div['class'] if cls.startswith('ed-')), None)
#     if key:
#         header = div.find('h3').text.strip() if div.find('h3') else None
#         text = [(idx, item.text.strip()) for idx, item in enumerate(div.select('li, o, p'), start=1)]
#         lang = div.get('lang')
#         data_label = div.get('data-label')
#         if header:
#             if key not in transcriptions:
#                 transcriptions[key] = {}
#             transcriptions[key][header] = {
#                 "text": text,
#                 "lang": lang,
#                 'data_label': data_label
#             }

# # Collect translations
# for div in soup.find_all('div', class_=lambda x: x and 'translation' in x):
#     key = next((cls for cls in div['class'] if cls.startswith('tr-')), None)
#     if key:
#         header = div.find('h3').text.strip() if div.find('h3') else None
#         text = [(idx, item.text.strip()) for idx, item in enumerate(div.select('li, o, p'), start=1)]
#         lang = div.get('lang')
#         data_label = div.get('data-label')
#         if header:
#             if key not in translations:
#                 translations[key] = {}
#             translations[key][header] = {
#                 "text": text,
#                 "lang": lang,
#                 'data_label': data_label
#             }

# print(translations)




transcriptions = {}
translations = {}

# Collect transcriptions
for div in soup.find_all('div', class_=lambda x: x and 'transcription' in x):
    key = next((cls for cls in div['class'] if cls.startswith('ed-')), None)
    if key:
        header = div.find('h3').text.strip() if div.find('h3') else None
        text = [item.text.strip() for item in div.select('li, o, p')]
        data_label = div.get('data-label')
        lang = div.get('lang')
        if header:
            transcriptions[header] = {
                "transcription": key,
                "text": text,
                'data_label': data_label,
                'lang': lang
            }

# Collect translations
for div in soup.find_all('div', class_=lambda x: x and 'translation' in x):
    key = next((cls for cls in div['class'] if cls.startswith('tr-')), None)
    if key:
        header = div.find('h3').text.strip() if div.find('h3') else None
        text = [item.text.strip() for item in div.select('li, o, p')]
        data_label = div.get('data-label')
        lang = div.get('lang')
        if header:
            translations[header] = {
                "translation": key,
                "text": text,
                'data_label': data_label,
                'lang': lang
            }

# Merge transcriptions and translations based on folio headers
folios = []
for header in transcriptions.keys():
    folio_entry = {
        "folio": header,
        "transcription": transcriptions[header]
    }
    if header in translations:
        folio_entry["translation"] = translations[header]
    folios.append(folio_entry)

# Print the results
for folio in folios:
    print(folio)



# transcriptions = []

# # Collect transcriptions
# for div in soup.find_all('div', class_=lambda x: x and 'transcription' in x):
#     key = next((cls for cls in div['class'] if cls.startswith('ed-')), None)
#     if key:
#         header = div.find('h3').text.strip() if div.find('h3') else None
#         text = [item.text.strip() for item in div.select('li, o, p')]
#         data_label = div.get('data-label')
#         lang = div.get('lang')
#         if header:
#             transcriptions.append(
#                 {"transcription": key, 
#                  "folio": header,
#                  "text": text,
#                  'data_label': data_label,
#                  'lang':lang
#                                    })

# translations = []

# # Collect translations
# for div in soup.find_all('div', class_=lambda x: x and 'translation' in x):
#     key = next((cls for cls in div['class'] if cls.startswith('tr-')), None)
#     if key:
#         header = div.find('h3').text.strip() if div.find('h3') else None
#         text = [item.text.strip() for item in div.select('li, o, p')]
#         data_label = div.get('data-label')
#         lang = div.get('lang')
#         if header:
#             translations.append(
#                 {"translation": key, 
#                  "folio": header,
#                  "text": text,
#                  'data_label': data_label,
#                  'lang':lang
                 
#                  }
#                  )
            

# # Print the results
# print(transcriptions)
# print(translations)


# for panel in translation_panels:
#     
#     translation_div= panel.find('div', class_=f'translation tr-{kms}')
#     if translation_div:
#         data_ittpanel_target = translation_div.get('data-ittpanel-target')
#         data_label = translation_div.get('data-label')
#         lang = translation_div.get('lang')

#         print(f"data-ittpanel-target: {data_ittpanel_target}")
#         print(f"data-label: {data_label}")
#         print(f"lang: {lang}")

#     else: print("You should kill yourself")


    # translation_data = {
    #     "text": [item.text.strip() for item in panel.select('li, o, p')],
    #     "data-translation": kms,
    #     #"data-label": panel.find('span', {'data-transcription-target': 'translationShortLabel'}).text.strip(),
    #     "lang": panel.find('div', class_=f'transcription tr-{kms}').get('lang', '')
    # }
    # translations.append(translation_data)


# print(transcriptions)
# print(translations)