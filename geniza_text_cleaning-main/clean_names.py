from unidecode import unidecode
import pandas as pd
import sys
import re




def normalize_name(test_name):
    # Remove diacritics and convert to ASCII
    test_name = unidecode(test_name)

    # Convert to lowercase for consistent processing
    test_name = test_name.lower()

    # Remove parentheses, brackets, and their contents
    test_name = re.sub(r'\([^)]*\)', '', test_name)

    # Remove apostrophes, quotation marks, and question marks
    test_name = re.sub(r'[\'"`?]', '', test_name)

    test_name = re.sub(r'\bl-', 'al-', test_name)


    # Standardize prefixes and honorifics
    prefixes = {
        r'\babu (?:l-|al-)?': 'abu ',
        r'\b(?:ibn|bin|ben|bar)\b': 'b.',
        r'\b(?:bint|ibnat|berat|bat)\b': 'bt.',
        r'\b(?:rav|rabbi|r\.)\b': '',
        r'\b(?:gaon|ga`on)\b': '',
        r'\b(?:hahaver|ha-haver|he-haver)\b': '',
        r'\b(?:nagid|ha-nagid)\b': '',
        r'\b(?:ha-kohen|hakohen)\b': '',
        r'\b(?:ha-levi|halevi)\b': '',
        r'\b(?:ha-parnas)\b': '',
        r'\b(?:ha-hazzan)\b': '',
        r'\b(?:ha-gevir)\b': '',
        r'\b(?:ha-melammed)\b': '',
        r'\b(?:ha-rosh nin ha-geonim)\b': '',
        r'\b(?:ha-mumhe)\b': '',
        r'\b(?:walad ha-nezer)\b': '',
        r'\b(?:ha-rofe)\b': '',
        r'\b(?:ha-najib)\b': '',
        r'\b(?:ha-sefardi)\b': '',
        r'\b(?:ha-sefaradi)\b': '',
        r'\b(?:the spaniard)\b': '',
        r'\b(?:the sefardi)\b': '',
        r'\b(?:the doctor)\b': '',
        r'\bbu\b': 'abu',
    }

    for pattern, replacement in prefixes.items():
        test_name = re.sub(pattern, replacement, test_name)

    #to do, if the name starts with "'", have the first english character capitalized
    # Dictionary of standardized name forms
    name_standardization = {
    "aharon": ["aaron"],
    "avon": ["abon"],
    "avraham": ["abraham", "avraha", "ibrahim"],
    "ʿazarya": ['azaraiah', 'azarya'],
    "binyamin": ['benjamin'],
    "boʿaz": ["boaz", "bo'az"],
    "baruch": ["barukh", "baruk"],  # Comment: Kept from original list, not in second list
    "daniʾel": ['daniel', "dani'el"],
    "david": ["daud", "dawud"],  # Comment: Kept from original list, not in second list
    "efrayim": ["ephraim", "ephrayim", "ifrayim"],
    "evyatar": ['ebiathar'],
    "elʿazar": ['eleazar', 'elazar', 'elizur', "el'azar"],
    "ʿeli": ['eli', "'eli"],
    "eliyyahu": ['elijah', 'eliyahu'],
    "ezra": ["ezrah", "azra"],  # Comment: Kept from original list, not in second list
    "ʿimmanuʾel": ['emmanuel', "immanuel", "'immanu'el"],
    "halfon": ["khalfon", 'khalfun'],  # Comment: Kept from original list, not in second list
    "hananel": ["hananeel", "hananiel"],  # Comment: Kept from original list, not in second list
    "ḥananya": ['hanania', 'hananiah', 'hanaia'],
    "hasan": ["hasun", "hassun", "hassan"],  # Comment: Kept from original list, not in second list
    "ḥayyim": ["haim", "chaim", "hayim"],
    "ḥasday": ["hasdai", "hisdai", "hisday", "hisda"],
    "ḥizqiyyahu": ["hezekiah"],
    "iyyov": ["job"],
    "kadmiʾel": ['cadmiel'],
    "kalev": ["caleb"],
    "khalluf": ["khalaf", "khalfa", "khulayf"],  # Comment: Kept from original list, not in second list
    "kohen": ["cohen"],
    "leʾa": ["leah"],
    "menaḥem": ["menachem"],
    "menashshe": ["manasseh", "menashshee", "mannaseh", "menase", "manashshe", "manasse", "menashe"],
    "meʾir": ["meir"],
    "mevorakh": ["mevorak"],  # Comment: Kept from original list, not in second list
    "mordekhay": ["mordechai"],
    "moshe": ["moses", "musa"],
    "naḥum": ["nachum"],
    "natan": ["nathan"],
    "neḥemya": ["nehemiah"],
    "netanʾel": ["nathaniel", "nethanel", "natanel"],
    "nissim": ["nisim"],  # Comment: Kept from original list, not in second list
    "peraħya": ["perahiah", "perah"],
    "pinḥas": ["phineas"],
    "rafaʾel": ["raphael"],
    "reʾuven": ["reuben"],
    "rivqa": ["rebecca"],
    "saʿadya": ["saadiah", "saada", "saadia", "saadyah", "seadya"],
    "said": ["sayyid"],  # Comment: Kept from original list, not in second list
    "salih": ["salah"],  # Comment: Kept from original list, not in second list
    "sasson": ["sason"],  # Comment: Kept from original list, not in second list
    "sadaqa": ["sedaqa", "sadaqah", "sadoq", "zedaqa", "zadaka"],  # Comment: Kept from original list, not in second list
    "shabbetay": ["sabbetai", "shabbatay"],
    "shaʾul": ["saul"],
    "shelomo": ["solomon", "shalom", "shlomo"],
    "shemaʿya": ["shemaiah"],
    "shemarya": ["shemariah", "shemaya", "semarya", "sehmarya"],
    "shemuʾel": ["samuel", "shemuel", "shmuel", "shemeul"],
    "shimʿon": ["simon", "simeon"],
    "sughmar": ["sighmar", "sigmar", "sugmar"],  # Comment: Kept from original list, not in second list
    "ṣefanya": ["zephaniah"],
    "ṣemaḥ": ["zemaḥ"],
    "ṭoviyya": ["tobias", "tovia", "toviya", "toviyya", "toviyyahu", "tuviyyahu", "tuvya"],
    "yaʿaqov": ["jacob", "yaaqov", "yaaqub", "yaaquv", "yaakob", "yaqub", "yaakov"],
    "yehoshuaʿ": ["joshua", "yehoshua", "yeshua", "yehoshuaha", "yoshua"],
    "yehuda": ["judah", "yehudah"],
    "yeḥezqel": ['ezekiel', "yequtiel"],
    "yeḥiʾel": ["jechiel", "jehiel"],
    "yequtiʾel": ["jekuthiel"],
    "yeshaʿyahu": ["isaiah"],
    "yeshuaʿ": ["jeshua"],
    "yiftaḥ": ["jephthah"],
    "yiṣḥaq": ["isaac", "yishaq", "yitzhak", "ishaq", "yizhak", "itzhak", "yizhaq", "yishak"],
    "yisrael": ["israel"],
    "yissakhar": ["issachar"],
    "yoʾel": ["joel"],
    "yoḥanan": ["john"],
    "yona": ["jonah"],
    "yonatan": ["jonathan"],
    "yosef": ["joseph", "yusuf", "yehosef"],
    "yoshiyyahu": ["josiah"],
    "zekharya": ["zechariah", "zakariya", "zakariyya", "zekharia", "zakarya", "zekhariya"],
    "berakot": ["barakat", "berakhot"],  # Comment: Kept from original list, not in second list
    "fustat": ["furat"],  # Comment: Kept from original list, not in second list
    "ghazzi": ["ghazzawi", "al-ghazzawi", "ha-gazzawi", "gazal"],  # Comment: Kept from original list, not in second list
    "jerusalem": ["ha-yerushalmi", "yerushalmi"],  # Comment: Kept from original list, not in second list
    "maqdisi": ["muqaddasi"],  # Comment: Kept from original list, not in second list
    "tripoli": ["ha-itrabulusi", "ha-atrabulsi", "ha-itrabulsi"],  # Comment: Kept from original list, not in second list
}

    # Complex name variations
    complex_names = {
        "Halfon b. Menashshe": [
            "Halfon b. Menashshe ha-Levi",
            "Halfon b. Menashshe halevi",
            "Halfon ha-Levi b. Menashshe",
            "Abu Said Halfon b. Menashshe",
            "Abu Said Halfon b. Menashshe al-Qata`if",
            "Halfon b. Menase Halevi"
        ],
        "Hillel b. Eli": [
            "Hillel ha-Hazzan b. Eli"
        ],
        "Mevorakh b. Natan": [
            "Mevorakh b. Natan ha-Haver",
            "Mevorakh b. Natan b. Shalom",
            "Mevorakh b. Natan b. Shalom Walad ha-Nezer",
            "Mevorakh b. Natan ha-Kohen",
            "Mevorakh b. Natan ha-Gevir",
            "Mevorakh b. Natan ha-Melammed"
        ],
        "Mevorakh b. Saadya": [
            "Mevorakh b. Saadya ha-Nagid",
            "Nagid Mevorakh b. Sadya",
            "Nagid Mevorakh b. Saadya",
            "Mevorakh b. Natan ha-Kohen",
            "Mevorakh b. Natan ha-Gevir",
            "Mevorakh b. Natan ha-Melammed"
        ],
        "Halfon b. Netanel ha-Levi": [
            "Halfon b. Netanel",
            "Halfon b. Netanel Halevi",
            "Halfon b. Natan ha-Levi"
        ],
        "Ulla ha-Levi b. Yosef": [
            "Ulla ha-Levi ha-Parnas b. Yosef",
            "Abu Ala Ulla ha-Levi b. Yosef",
            "Ulla b. Yosef",
            "Ulla Ha-Levi Ha-Parnas b. Yosef"
        ],
        "Moshe b. Levi ha-Levi": [
            "Moshe b. Levi",
            "Moshe b. Levi Halevi",
            "Moshe ha-Levi b. Levi ha-Haver"
        ],
        "Yosef b. Moshe b. Barhun ha-Tahirti": [
            "Yosef b. Moshe Tahirti",
            "Yosef b. Moshe",
            "Abu Said Yosef b. Moshe b. Barhun",
            "Abu Said Yosef b. Moshe ha-Taherti",
            "Yosef b. Moshe ha-Tahirati",
            "Yosef b. Moshe ha-Taherti",
            "Yosef b. Moshe ha-Tahirti"
        ],
        "Yehuda b. Yosef": [
            "Abu Zikri Yehuda b. Yosef ha-Kohen",
            "Yehuda b. Yosef ha-Kohen",
            "Abu Zikri Yehuda b. Yosef",
            "Yehuda b. Yosef Abu Zikri",
            "Abu Zekharia Yehuda b. Yosef Hakohen",
            "Yehuda b. Yosef Sijilmasi"
        ],
        "Abraham b. Moshe": [
            "Abraham b. Moshe ha-Kohen",
            "Abu Yishaq Abraham b. Moshe",
            "Abraham b. Moshe Levi"
        ],
        "Nissim b. Yishaq ha-Tahirti": ["Nissim b. Yishaq", "Nissim b. Yishaq b. ha-Sahl", "Nissim b. Yishaq b. Alsahl"],
        "Shalom b. Saadya ha-Levi": [
            "Shalom b. Saadya",
            "Shalom ha-Levi b. Saadya"
        ],
        # New names added
        "Moshe b. Abi ha-Hayy": [
            "Moshe b. Abi l-Hayy",
            "Abu Imran Moshe b. Abi l-Hayy",
            "Moshe b. Abi ha-Hayy Khalila",
            "Moshe b. Abi l-Hayy Khalila",
            "Abu Imran Moshe b. Abi l-Hayy b. Khalila",
            "Moshe b. Abi ha-Hay"
        ],
        "Yosef b. Abraham ha-Iskandarani": [
            "Yosef b. Abraham",
            "Yosef b. Abraham b. Sfus",
            "Abu Yaaqov Yosef b. Abraham"
        ],
        "Yehuda ha-Levi": [
            "R. Yehuda ha-Levi",
            "Abu Nasr Yehuda ha-Levi b. Yehoshua"
        ],
        "Natan b. Yosef": [
            "Natan b. Yosef ha-Kohen",
            "Natan b. Yosef ha-Baradani"
        ],
        "Halfon ha-Kohen b. Elazar": [
            "Halfon b. Elazar ha-Kohen"
        ],
        "Elazar ha-Kohen b. Shalom": [
            "Elazar ha-Kohen",
            "Elazar ha-Kohen b. Shalom ha-Rosh Nin ha-Geonim",
            "Elazar Ha-Kohen Ha-Mumhe"
        ]
    }

    # Split the name into parts
    name_parts = test_name.split()

    # Normalize each part of the name
    normalized_parts = []
    for part in name_parts:
        normalized = part
        for standard, variations in name_standardization.items():
            if part in variations:
                normalized = standard
                break
        normalized_parts.append(normalized)

    # Join the normalized parts
    normalized_name = " ".join(normalized_parts)

    # Remove duplicates (e.g., "ha-levi ha-levi")
    normalized_name = re.sub(r'\b(.+?)\s+\1\b', r'\1', normalized_name)

    # Handle special cases
    if ("maimonides" in normalized_name or "rambam" in normalized_name) and "abraham" not in normalized_name:
        normalized_name = "moses maimonides"

    # Capitalize the first letter of each word
    normalized_name = ' '.join(word.capitalize() for word in normalized_name.split())

    for standard_name, variations in complex_names.items():
        if any(variation.lower() in normalized_name.lower() for variation in variations):
            return standard_name

    return normalized_name

#normalizes all the names in the list of names
def normalize_single_document_names(list_of_names):
    return [normalize_name(name) for name in list_of_names]


#normaliez all names in all documents fed into it
def normalize_all_names(data):
    # Normalizes all names in the "names" field
    data['names'] = [normalize_single_document_names(names) for names in data['names']]

    # If there are one or more authors, clean their names
    if 'author' in data:
        data['author'] = data['author'].apply(lambda author: [normalize_name(a) for a in author] if isinstance(author, list) else normalize_name(author))

    # If there are one or more recipients, clean their names
    if 'recipient' in data:
        data['recipient'] = data['recipient'].apply(lambda recipient: [normalize_name(r) for r in recipient] if isinstance(recipient, list) else normalize_name(recipient))

    return data

#create a sorted list of grouped pgpids and which names are associated with them
def group_pgpids_by_name(data_out):
    # Select relevant columns and explode the names
    data_out_names = data_out[['pgpid', 'names']]
    names_exploded = data_out_names.explode('names').reset_index(drop=True)

    # Group by names and aggregate pgpid into a list
    grouped_names = names_exploded.groupby('names')['pgpid'].apply(list).reset_index()

    # Rename columns for clarity
    grouped_names.columns = ['name', 'pgpids']

    # Add a new column with the count of pgpids (optional, for sorting purposes)
    grouped_names['pgpid_count'] = grouped_names['pgpids'].apply(len)

    # Sort by the count of pgpids in descending order
    sorted_grouped_names = grouped_names.sort_values(by='pgpid_count', ascending=False).reset_index(drop=True)

    # Keep only the 'name' and 'pgpids' columns
    sorted_grouped_names = sorted_grouped_names[['name', 'pgpids']]

    return sorted_grouped_names

    

def main(data):
    data_out = normalize_all_names(data)
    sorted_grouped_names = group_pgpids_by_name(data_out)
    
    sorted_grouped_names.to_csv("grouped_names.csv",index=False)
    data_out.to_csv("cleaned_documents.csv", index=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_names.py <documentlist.csv> | <documentlist.json>")
        sys.exit(1)
    documents = sys.argv[1]
    document_name, extension = documents.split(".")
    if extension == "json":
        data = pd.read_json(documents)
    elif extension == "csv":
        data = pd.read_csv(documents)
    else:
        print("Usage: python clean_names.py <documentlist.csv> | <documentlist.json>")
        sys.exit(1)
    
    main(data)