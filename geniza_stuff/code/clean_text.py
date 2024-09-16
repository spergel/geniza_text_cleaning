import re
import json
def condense_paragraphs(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        paragraphs = input_file.read().split('\n\n')  # Split into paragraphs

    condensed_paragraphs = []
    for paragraph in paragraphs:
        lines = paragraph.strip().split('\n')  # Split paragraph into lines
        condensed_paragraph = ' '.join(lines)
        # Use regular expressions to extract relevant information
        condensed_paragraphs.append(get_page_number_from_body(condensed_paragraph))

    with open(output_filename, 'w') as output_file:
        output_file.write(''.join(condensed_paragraphs))  # Join paragraphs with double newline
def get_page_number_from_body(text):
    # Extract page number from body text
    print
    page_number = re.search(r'\b(\d{1,3})\b', text).group(0)
    # Remove page number from body text
    text = re.sub(r'\b(\d{1,3})\b', '', text)
    # Add page number to metadata
    metadata = {'page_number': page_number}
    text_data = {'text': text}
    result = {**metadata, **text_data}
    # Return JSON string
    return json.dumps(result, indent=2) + '\n\n'


input_file = "/Users/joshs/Desktop/ai_stuff/geniza_stuff/data/book_2/chapter_5.md"  # Replace with your input file name
output_file = "/Users/joshs/Desktop/ai_stuff/geniza_stuff/data/book_2/chapter_5.json"  # Replace with your output file name
condense_paragraphs(input_file, output_file)