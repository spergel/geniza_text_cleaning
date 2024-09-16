import pandas as pd
from openai import OpenAI
file_path = "/Users/joshs/Desktop/ai_stuff/geniza_stuff/geniza_transliterations.csv"
df = pd.read_csv(file_path, header=None, encoding='utf-8')

cols = ['pgpid', 'text']
df.columns = cols
# Define your OpenAI API key
api = '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'
js = pd.DataFrame(columns=['pgpid', 'original text','translated_text'])
# Define the ChatGPT prompt
def get_info(input_text):
    prompt = f"""
    The following is a text in either Arabic, Hebrew, or Judeo-Arabic. Acting as an expert translator, translate the document directly into English without any additional commentary:
    """ 

    # Initialize the OpenAI API client
    

    # Call ChatGPT to extract information
    client = OpenAI(api_key=api)
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role":"system","content":f'{prompt}'},
        {"role":"user","content": f'{input_text}'}
    ],
    max_tokens=4096,  # Adjust max tokens as needed
    temperature=0.1  # Adjust temperature as needed
    )
    return response

for ind, row in df.iterrows():
    translated_text = get_info(row['text'])
    print(translated_text)
    js.loc[len(js)] = [row['pgpid'], row['text'],translated_text]
    
print(js)

js.to_csv('test.csv',index=False)  