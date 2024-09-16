README
Overview
This script normalizes names in a given document list (CSV or JSON format) and outputs the cleaned data along with grouped names and associated pgpids.

Prerequisites
Ensure you have Python installed. You also need the following Python packages:

pip install pandas unidecide

Usage:
To run the script, use the following command:
python clean_names.py <documentlist.csv> | <documentlist.json>


For example:
python clean_names.py all_documents.json
