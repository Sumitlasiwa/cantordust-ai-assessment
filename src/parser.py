import os
import pdfplumber

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

def extract_text_from_pdfs_through_directory(input_dir, output_dir):
    """
    Loops through all PDF files in the input directory, extracts text, and saves it to the output directory.

    Args:
        input_dir (str): The directory containing PDF files.
        output_dir (str): The directory where extracted text files will be saved.
    """
    for i, pdf in enumerate(sorted(os.listdir(input_dir))):
        if pdf.endswith(".pdf"):
            input_path = os.path.join(input_dir, pdf)
            output_path = os.path.join(output_dir, f"parsed_text_{i+1}.txt")
            text = extract_text_from_pdf(input_path)
            save_text_to_file(text, output_path)
            print(f"Extracted text from {input_path} to {output_path}")

if __name__ == "__main__":
    extract_text_from_pdfs_through_directory("data/raw", "data/processed")

