import pandas as pd
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from groq import Groq
import instructor
import os
class LegalWithWitnesses(BaseModel):
    pgpid: int
    original_location: Optional[str] = Field(..., description="The location where the document was composed")
    validation_location: Optional[str] = Field(..., description="The location where the document was validated, if mentioned")
    date: str = Field(..., description="The date the document was authored as stated in the text")
    date_standard: str = Field(..., description="The date of the letter in the format {YYYY-MM-DD}")
    author: str = Field(..., description="The name of the author who composed the document")
    scribe: Optional[str] = Field(..., description="The name of the scribe who composed the document, if separate from the author")
    original_witnesses: Optional[List[str]] = Field(..., description="The names of the witnesses who signed the document")
    verifying_witnesses: Optional[List[str]] = Field(..., description="The names of the witnesses who validation the document, if there is a separate validation")
    names: List[str] = Field(..., description="A list of names in the document")
    note: Optional[str] = Field(..., description="Any notes or comments about the extracted information")

class Letter(BaseModel):
    pgpid: int
    names: List[str] = Field(..., description="A list of names in the document")
    start_location: str = Field(..., description="The location where the document was composed")
    end_location: str = Field(..., description="The location where the document sent")
    mentioned_locations: List[str] = Field(..., description="A list of locations mentioned in the document, if separate from the start and end destinations")
    date: str = Field(..., description="The date the document was authored as stated in the text. a general time period should be {startdate}/{enddate}")
    date_standard: str = Field(..., description="The date of the letter in the format {YYYY-MM-DD}")
    author: str = Field(..., description="The name of the author who composed the document")
    recipient: str = Field(..., description="The name of the recipient of the document")

def process_geniza_documents(input_file: str, output_file: str, document_type: str):
    df = pd.read_csv(input_file, on_bad_lines='skip')
    df = df[['pgpid', 'type', 'description']]
    
    df['count'] = (df['description'].str.count(' b. ') +
                   df['description'].str.count(' ibn ') +
                   df['description'].str.count(' the judge ') +
                   df['description'].str.count(' al') +
                   df['description'].str.count(' abu'))
    df = df[df['count'] >= 2]

    groq = Groq(api_key=os.getenv('GROQ_API_KEY'))
    client = instructor.from_groq(groq, mode=instructor.Mode.TOOLS)

    def get_info(prompt):
        resp = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            response_model=LegalWithWitnesses if document_type == 'legal' else Letter,
        )
        return json.loads(resp.model_dump_json(indent=2))

    results = []
    for doc in df.to_dict('records'):
        geniza_test = doc['description']
        pgp_id = doc['pgpid']
        prompt = f"""
        You are a Cairo Geniza expert tasked with extracting historical data from the provided {document_type} text description.
        Please extract and return the following details in JSON format:

        Guidelines:
        1. Extract all relevant information based on the Pydantic model.
        2. Use 'N/A' for any unknown or unavailable information.
        3. Ensure all names include patronymics and descriptors when available.
        4. For date ranges, use the format 'startdate/enddate' in both 'date' and 'date_standard' fields.
        5. Include all mentioned locations in 'mentioned_locations', except those already listed in start_location and end_location.
        6. Names typically include patronymics such as 'b.', 'ibn', or descriptors like 'al-[location]'. Be sure to include full names instead of partial names when they are available. Do not list names twice if they are a full name and partial name (e.g. do not list Barhun b. Ishaq and Barhun if they are clearly the same person)

        Input: pgpid: '{pgp_id}', description: '{geniza_test}'
        Output:
        """
        data = get_info(prompt)
        print(data)
        results.append(data)

    output_df = pd.DataFrame(results)
    output_df.to_json(output_file, orient='records')

if __name__ == "__main__":
    input_file = "documents.csv"
    output_file = "processed_geniza_documents.json"
    document_type = "legal"  # Change to "letter" for processing letters
    process_geniza_documents(input_file, output_file, document_type)