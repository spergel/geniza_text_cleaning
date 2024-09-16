import pandas as pd

# Read the JSON file
df = pd.read_json("created_data/all_documents.json")

names_x = [
    "Nahray b. Nissim",
    "Halfon b. Menashshe",
    "Moses Maimonides",
    "Efrayim b. Shemarya",
    "Shelomo b. Yehuda",
    "Shelomo b. Eliyahhu",
    "Hillel b. Eli",
    "Moshe b. Levi",
    "Mevorakh b. Natan",
    "Daniel b. Azarya"
]

# Create new columns for each name
for name in names_x:
    df[name] = df['names'].apply(lambda x: name in x if isinstance(x, list) else False)

# Select the desired columns
new_df = df[["pgpid"] + names_x]

# Save the result to a CSV file
new_df.to_csv("output.csv", index=False)