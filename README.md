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

`src/graph_visualizer.py` renders this compiled LangGraph workflow as
`workflow_graph.png`. `src/main.py` calls it after the pipeline completes, so
the repository includes a visual representation of the workflow as well as the
code that defines it.

## Architecture

```text
Manufacturer PDF URLs
        |
        v
  requests downloads PDFs
        |
        v
pdfplumber extracts selectable text ──> data/processed/*.txt
        |
        v
Gemini extracts the `ProductInfo` schema ──> outputs/extracted/*.json
        |
        v
Deterministic comparison, with Gemini only for ambiguous values
        |
        v
Markdown comparison report
```

### Why extract text with `pdfplumber` before using the LLM?

The pipeline deliberately does not send each PDF directly to an LLM and ask it
to return JSON. `pdfplumber` first extracts the selectable text locally, and
the LLM then performs the narrower task of mapping that text to the predefined
`ProductInfo` schema.

This separation has several benefits:

- **Inspectable intermediate data.** The extracted text is saved under
  `data/processed/`, so an unexpected JSON value can be traced back to the
  source text used by the model.
- **More predictable LLM input.** Plain text avoids depending on a model's PDF
  document-ingestion behavior and lets the prompt focus on field extraction.
- **Lower coupling and easier testing.** PDF parsing can be tested, replaced,
  or enhanced independently from the Gemini extraction and comparison stages.
- **Controlled use of the LLM.** The model receives text rather than a binary
  document and is also limited to a Pydantic-defined response schema; simple
  comparisons remain local and deterministic.

The tradeoff is that text-only extraction can lose layout and table structure,
and it does not support image-only scanned PDFs. A direct multimodal PDF-to-JSON
approach may preserve visual context for those documents, but makes extraction
less inspectable and more dependent on the model's document parsing. For this
assessment's selectable-text manufacturer datasheets and fixed comparison
schema, the staged approach favors reproducibility and debuggability.

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
│   ├── graph_visualizer.py  # Renders the LangGraph workflow to workflow_graph.png
│   ├── fetcher.py           # Downloads PDFs from configured URLs
│   ├── parser.py            # Extracts text from PDFs
│   ├── extractor.py         # Extracts predefined product fields with Gemini
│   ├── comparator.py        # Compares fields and uses Gemini for ambiguity
│   ├── report_generator.py  # Produces the Markdown report
│   └── llm_client.py        # Shared Gemini client
├── .env.example             # Required environment variable template
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project metadata and dependencies
└── workflow_graph.png       # Generated visualization of the LangGraph workflow
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
