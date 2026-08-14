import os
import pdfplumber

def extract_text_from_pdf_and_save(input_path, output_path):
    """
    Extracts text from a PDF file using pdfplumber.

    Args:
        input_path (str): The path to the PDF file.
        output_path (str): The path to the output text file.
    """
    with pdfplumber.open(input_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    with open(output_path, "w") as f:
        f.write(text)

if __name__ == "__main__":
    for i, pdf in enumerate(sorted(os.listdir("data/raw"))):
        if pdf.endswith(".pdf"):
            input_path = os.path.join("data/raw", pdf)
            output_path = os.path.join("data/processed", f"parsed_text_{i+1}.txt")
            extract_text_from_pdf_and_save(input_path, output_path)
            print(f"Extracted text from {input_path} to {output_path}")

