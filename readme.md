# Geniza Document Tools

This project provides tools for scraping, processing, and analyzing Geniza documents. It includes functionality for web scraping, text cleaning, and AI-powered information extraction.

## Project Structure

- `geniza_scraper.py`: Web scraper for Geniza documents.
- `clean_text.py`: Text cleaning and processing utility.
- `geniza_processor.py`: AI-powered information extraction from Geniza document descriptions.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/geniza-document-tools.git
   cd geniza-document-tools
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root directory with the following content:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Replace `your_groq_api_key_here` with your actual Groq API key.

## Usage

### Geniza Document Scraper

To scrape Geniza documents:
python geniza_scraper.py [--pgpid PGPID] [--all] [--transcriptions] [--translations]


Arguments:
- `--pgpid PGPID`: Scrape a specific document by its PGPID.
- `--all`: Scrape all documents.
- `--transcriptions`: Include documents with transcriptions (use with --all).
- `--translations`: Include documents with translations (use with --all).

### Text Cleaner

To clean and condense text from a markdown file:

1. Open `clean_text.py` and modify the `input_file` and `output_file` variables.
2. Run the script:
   ```
   python clean_text.py
   ```

### Geniza Processor

To process Geniza documents and extract information:

1. Prepare your input CSV file with columns: 'pgpid', 'type', and 'description'.
2. Ensure your Groq API key is set in the `.env` file.
3. Run the script:
   ```
   python geniza_processor.py
   ```

You can modify the `input_file`, `output_file`, and `document_type` variables in the script to customize the processing.


### Text Cleaning

To clean and process text:
python clean_text.py [--input INPUT_FILE] [--output OUTPUT_FILE]