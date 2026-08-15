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

## Workflow orchestration

The pipeline is orchestrated with LangGraph. `src/main.py` supplies the two PDF
URLs and the report path, then invokes the compiled graph in `src/graph.py`.

```text
fetch PDFs → parse PDF text → extract product fields → compare fields → generate report
```

LangGraph passes one shared workflow state between these nodes. The state holds
the input URLs, paths to downloaded PDFs and extracted text, paths to the
extracted JSON files, the comparison result path, and the final report path.
This makes the pipeline steps explicit and gives the project a clear place to
add branching, retries, validation, or additional processing steps later.

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
│   ├── graph.py             # LangGraph workflow and pipeline nodes
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
- `langgraph` — orchestrates the fetch, parse, extract, compare, and report
  steps as a stateful workflow.

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
