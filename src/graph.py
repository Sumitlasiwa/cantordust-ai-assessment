from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from fetcher import download_pdf
from parser import extract_text
from extractor import extract_fields
from comparator import compare_fields
from report_generator import generate_report

class WorkflowState(TypedDict):
    pdf_urls: List[str]     # URLs to download
    pdf_paths: List[str]    # local downloaded PDFs
    text_paths: List[str]   # extracted text files
    extracted_paths: List[str]  # extracted JSON files
    comparison_path: str    # comparison result
    report_path: str    # final report

def fetch_node(state: WorkflowState) -> WorkflowState:
    state["pdf_paths"] = download_pdf(urls=state["pdf_urls"], out_dir="data/raw")
    return state

def parse_node(state: WorkflowState) -> WorkflowState:
    state["text_paths"] = extract_text(pdf_paths=state["pdf_paths"], output_dir="data/processed")
    return state

def extract_node(state: WorkflowState) -> WorkflowState:
    state["extracted_paths"] = extract_fields(text_paths=state["text_paths"], output_dir="outputs/extracted")
    return state

def compare_node(state: WorkflowState) -> WorkflowState:
    state["comparison_path"] = compare_fields(extracted_paths=state["extracted_paths"], output_dir="outputs/comparisons")
    return state

def report_node(state: WorkflowState) -> WorkflowState:
    state["report_path"] = generate_report(comparison_json_path=state["comparison_path"], output_md_path=state["report_path"])
    return state

builder = StateGraph(WorkflowState)

builder.add_node("fetch", fetch_node)
builder.add_node("parse", parse_node)
builder.add_node("extract", extract_node)
builder.add_node("compare", compare_node)
builder.add_node("report", report_node)

builder.set_entry_point("fetch")

builder.add_edge("fetch", "parse")
builder.add_edge("parse", "extract")
builder.add_edge("extract", "compare")
builder.add_edge("compare", "report")
builder.add_edge("report", END)

graph = builder.compile()