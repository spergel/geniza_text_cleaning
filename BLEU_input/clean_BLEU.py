import re
import os
import glob
import json

def process_text(text, language_specific_words):
    """
    Process the given text, removing lines containing language specific words
    and text within brackets.
    """
    # Split the text into lines
    lines = text.strip().split('\n')

    # Remove unwanted lines and text within brackets
    processed_text = []
    for line in lines:
        if any(word.lower() in line.lower() for word in language_specific_words):
            continue
        line = re.sub(r"\[.*?\]", "", line)  # Remove square brackets and content
        line = re.sub(r"[\(\)]", "", line)  # Remove parentheses

        words = line.strip().split()
        if words:
            processed_text.append(words)

    return processed_text

def process_files(input_dir, output_dir, language_specific_words):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all .txt files in the input directory
    for file_path in glob.glob(os.path.join(input_dir, '*.txt')):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Process the text
        processed_text = process_text(text, language_specific_words)

        # Generate the output file name based on the input file name
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file_path = os.path.join(output_dir, f"{base_name}.json")

        # Write processed text to the output JSON file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(processed_text, file, ensure_ascii=False, indent=2)

def main(input_dir, output_dir, language_specific_words):
    # Call the processing function
    process_files(input_dir, output_dir, language_specific_words)

if __name__ == "__main__":
    current_directory = os.getcwd()
    language_specific_words = ["recto", "verso", "margin"]  # Example words to remove
    
    # Define the input and output directories
    input_dir = os.path.join(current_directory, "input_texts")
    output_dir = os.path.join(current_directory, "individual_jsons")
    
    # Run the main function
    main(input_dir, output_dir, language_specific_words)
