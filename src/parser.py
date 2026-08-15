import os
import pdfplumber
from typing import List
def extract_text_from_pdf(input_path):
    """
    Extracts text from a PDF file using pdfplumber.

    Args:
        input_path (str): The path to the PDF file.
    """
    with pdfplumber.open(input_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text


def save_text_to_file(text, output_path):
    """
    Saves the extracted text to a specified file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(text)

def extract_text(pdf_paths: List[str], output_dir: str) -> List[str]:
    """
    Loops through all PDF files in the input directory, extracts text, and saves it to the output directory.

    Args:
        pdf_paths List(str): paths of pdf files.
        output_dir (str): The directory where extracted text files will be saved.
    """
    text_paths = []
    for i, pdf_path in enumerate(pdf_paths, start=1):
        output_path = os.path.join(output_dir, f"parsed_text_{i}.txt")
        text = extract_text_from_pdf(pdf_path)
        save_text_to_file(text, output_path)
        print(f"Extracted text from {pdf_path} to {output_path}")
        text_paths.append(output_path)

    return text_paths

if __name__ == "__main__":
    extract_text(["data/raw/datasheet_1.pdf", "data/raw/datasheet_2.pdf"], "data/processed")

