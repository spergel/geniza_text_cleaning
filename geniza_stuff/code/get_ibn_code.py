import pandas as pd
import json
import openai
import unicodedata
# API key and endpoint
client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = "esecret_2fiq3yggj78a759vxrl88zp62n")
input = "/Users/joshs/Documents/GitHub/Cairo_Geniza_Text/geniza_stuff/pgp_docs_only_desc.csv"
output = "/Users/joshs/Documents/GitHub/Cairo_Geniza_Text/geniza_stuff/pgp_descs"

# Function to normalize names
def normalize_name(name):

  test_name = unicodedata.normalize('NFKD', name)
  test_name = test_name.encode('ascii', 'ignore')
  test_name = test_name.decode('utf-8')
  full_name = test_name.split()
  all_names = {
        "Abraham": ["Abraham", "Avraham", "Avraha"],
        "Barukh": ["Barukh", "Baruk", "Baruch"],
        "Efrayim": ["Efrayim", "Ephraim", "Ephrayim"],
        "David": ["David", "Daud", "Dawud"],
        "Hasan": ["Hasan", "Hasun", "Hassun"],
        "Khalluf": ["Khalluf", "Khalfun", "Khalaf", "Khalfa", "Khulayf"],
        "Mevorakh": ["Mevorakh", "Mevorak"],
        "Moshe": ["Moshe", "Musa"],
        "Menasche": ["Menasche", "Manasche"],
        "Natan": ["Natan", "Nathan", "Nahum"],
        "Netanel": ["Netanel", "Nethanel", "Natanel", "Nathaniel"],
        "Saadya": ["Saadya", "Saada", "Saadyah", "Seadya"],
        "Sadaqa": ["Sadaqa", "Sedaqa", "Sadaqah", "Sadoq"],
        "Shelomo": ["Shelomo", "Shemuel"],
        "Shemarya": ["Shemarya", "Shemariah", "Shemaya"],
        "Sughmar": ["Sughmar", "Sighmar"],
        "Tovia": ["Tovia", "Toviya", "Toviyya", "Toviyyahu", "Tuviyyahu", "Tuvya"],
        "Yaaqov": ["Yaaqov", "Jacob", "Yaqub", "Yaakov"],
        "Yehoshua": ["Yehoshua", "Yeshua", "Yehoshuaha", "Yoshua"],
        "Yishaq": ["Yishaq", "Yitzhak", "Ishaq", "Yizhak", "Isaac"],
        "Yisrael": ["Yisrael", "Israel"],
        "Yosef": ["Yosef", "Joseph", "Yusuf", "Yehosef"]
    }
  n = 0
  for n in range(len(full_name)):
    for normalized_name, substrings in all_names.items():
        for substring in substrings:
            if substring in full_name[n]:
              full_name[n] = normalized_name
  return " ".join(full_name)

# Function to extract information using ChatGPT
def get_info(text, pgpid):
  prompt = f"""
    For the provided historical document, extract and compile the following information:
    * Names of all unique individuals mentioned
    * Location where it was composed
    * Date it was authored

    Focus on identifying primary authors, not modern scholars. Include signatories and key figures.
    Indicate "N/A" for unknown information. Names often contain "b.", "ibn", or similar designations.
    Distinguish between original document authors and modern analysts.

    Format the data as JSON:
    {{"pgpid": NNNN,"names": [list of names],"location": "document's location",
    "date": "document's date","date_standard": "date in Common Era","author": "primary author's name"}}

    Input:
    Four (?) court records in the hand of Natan ha-Kohen b. Shelomo. Fustat September 1133:
    a: Court prohibits Yosef b. Avraham from entering a compound (penalty: 10 dinars).
    b: Contract of rent: Abu Ali rents part of a house to Abu al-Fadl for 1 2/3 dirhams/month.
    c: Transfer of debt: 2 1/3 dinars owed by Yaʿaqov b. al-Shomer to Makarim (?) b. Yahya al-Hakim,
       paid by Husein b. Abu al-Faraj in installments.
    d: Excommunicated person advised by the court to settle disagreement within 50 days or pay a fine.

    Output:
    {{"pgpid": 2133,
    "names": ["Natan ha-Kohen b. Shelomo","Yosef b. Avraham", "Abu Ali", "Abu al-Fadl","Husein b. Abu al-Faraj","Yaʿaqov b. al-Shomer","Makarim b. Yahya al-Hakim"],
    "location": "Fustat",
    "date": "September 1133","date_standard": "1133 CE",
    "author": "Natan ha-Kohen b. Shelomo"}}

    Input: "pgpid":{pgpid}, {text}
    Output: 
    """

  chat_completion = client.chat.completions.create(
  model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that outputs in JSON."},
        {"role": "user", "content": prompt}
    ],
    response_format={
        "type": "json_object",
        "schema": {
            "type": "object",
            "properties": {
                "team_name": {"type": "string"}
            },
            "required": ["team_name"]
        },
    },
    temperature=0.1
  )
  print(chat_completion.model_dump()['choices']['message']['content'])
  return chat_completion.model_dump()['choices']['message']['content']

# Load data from CSV

initial_df = pd.read_csv(input)
def find_documents(df):
    df['count'] = df['description'].str.count(' b. ') + df['description'].str.count(' ibn ')
    df = df[df['count'] >= 1]
    return df
df = find_documents(initial_df)
with open("only_ibnb.json", "w") as f:
    json.dump(df, f, indent=4)

# Process each document
data = []
for index, row in df.iterrows():
    text, pgp_id = row["description"], row["pgpid"]
    info = get_info(text, pgp_id)
    data.append(info)

# Save extracted information
with open("extracted_data.json", "w") as f:
    json.dump(data, f, indent=4)

# Standardize names (optional, replace with your normalization logic)
for item in data:
    item["names"] = [normalize_name(name) for name in item["names"]]

# Save standardized data (optional)
with open("standardized_data.json", "w") as f:
   json.dump(f)