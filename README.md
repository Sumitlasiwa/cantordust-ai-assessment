# CantorDust AI Assessment

This project compares product specification PDFs from manufacturers. It downloads
two datasheets, extracts their text, uses Gemini to extract selected product
fields, compares the extracted values, and creates a Markdown report of matches,
differences, and fields that need review.

## Run the project

Prerequisite: Python 3.14 or later and a Google Gemini API key.

```bash
git clone https://github.com/Sumitlasiwa/cantordust-ai-assessment.git
cd cantordust-ai-assessment

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Add your API key to `.env`:

```env
GOOGLE_API_KEY="your_api_key_here"
```

Run the complete pipeline:

```bash
python src/main.py
```

The final report is written to `outputs/reports/final_report.md`.

## Project structure

```text
.
├── data/
│   ├── raw/                 # Downloaded PDF datasheets
│   └── processed/           # Text extracted from the PDFs
├── outputs/
│   ├── extracted/           # Product fields extracted as JSON
│   ├── comparisons/         # JSON comparison result
│   └── reports/             # Final Markdown report
├── src/
│   ├── main.py              # Runs the complete pipeline
│   ├── fetcher.py           # Downloads PDFs from configured URLs
│   ├── parser.py            # Extracts text from PDFs
│   ├── extractor.py         # Extracts predefined product fields with Gemini
│   ├── comparator.py        # Compares fields and uses Gemini for ambiguity
│   ├── report_generator.py  # Produces the Markdown report
│   └── llm_client.py        # Shared Gemini client
├── .env.example             # Required environment variable template
├── requirements.txt         # Python dependencies
└── pyproject.toml           # Project metadata and dependencies
```

## Important libraries

- `google-genai` — calls the Gemini API for structured field extraction and
  ambiguous semantic comparisons.
- `pydantic` — defines the expected product-field schema and structured LLM
  responses.
- `pdfplumber` — extracts text from PDF files.
- `requests` — downloads manufacturer datasheets.
- `python-dotenv` — loads `GOOGLE_API_KEY` from `.env`.

## Assumptions and limitations

- PDFs are assumed to contain selectable text; scanned PDFs are not supported.
- PDF tables are not preserved by the current text parser, which can affect
  extraction quality.
- The project extracts only the predefined fields in `ProductInfo`, not every
  specification in a datasheet.
- The current pipeline is configured to compare only two documents.
- LLMs are used for field extraction and for only part of the comparison: the
  code first resolves exact and simple deterministic matches locally.

## Future enhancements

- Use OCR-based PDF parsers to support scanned documents.
- Preserve table structure while extracting text from PDFs.
- Extract and compare all important product fields rather than a fixed schema.
- Support comparison of any number of documents.
