
import json
import pandas as pd

file_path = '/Users/joshs/Desktop/ai_stuff/geniza_stuff/pgp_docs.csv'
new_file_path = '/Users/joshs/Desktop/ai_stuff/geniza_stuff/pgp_docs_only_desc.csv'
df = pd.read_csv(file_path)


# Select required columns: 'pgpid', 'shelfmark', 'description'
df_selected = df[['pgpid', 'shelfmark', 'description']]
# Display the selected data
df_selected.to_csv(new_file_path,index=False)