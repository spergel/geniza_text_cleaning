import pandas as pd

# This Code does one thing. It takes an existing csv file and returns a csv with only the " ibn " or " b. " in order to get documents with named people.
def find_documents(csv_file):
    df = pd.read_csv(csv_file,on_bad_lines='skip')
    df['count'] = df['description'].str.count(' b. ') + df['description'].str.count(' ibn ')
    df = df[df['count'] >= 1]
    return df