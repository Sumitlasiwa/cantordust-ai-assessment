from google import genai
from google.genai import types
from llm_client import get_genai_client
from pydantic import BaseModel, Field
from typing import List, Optional
import dotenv
import json
import os

dotenv.load_dotenv()

def normalize(value):
    """
    Normalize the value for comparison according to the schema.
    """
    if isinstance(value, str):
        return value.strip().replace(" ", "").upper()
    elif isinstance(value, list):
        return sorted(normalize(v) for v in value)
    else:
        return value

from typing import TypedDict, Literal
from pydantic import Field

class Status(TypedDict):
    status: Literal[
        "match",
        "possible match",
        "conflict"
    ]
    confidence: float
    reason: str

def llm_compare(field, val1, val2):
    """
    Use a language model to compare two values and return the comparison result.
    """
    # Placeholder for LLM comparison logic
    client = get_genai_client()

    prompt = f"""
    You are comparing specifications from two manufacturer documents.

    Field: {field}

    Value 1:
    {val1}

    Value 2:
    {val2}

    Classify as:

    - match: same meaning
    - possible match: likely same but uncertain
    - conflict: genuinely different

    Be conservative.
    Do not assume equivalence unless supported.

    Return JSON only.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Status,
        ),
    )
    
    result = json.loads(response.text)
    return result 

def compare_documents(doc1, doc2):
    """
    Compare two documents and return the comparison results.
    """
    schema_fields = set(doc1.keys()).union(set(doc2.keys()))

    comparison_results = {}

    for field in schema_fields:
        val1 = doc1.get(field)
        val2 = doc2.get(field)

        response = None

        if normalize(val1) == normalize(val2):
            status = "match"
        elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            status = "conflict" if val1 != val2 else "match"
        elif val1 is None:
            status = "only in doc2"
        elif val2 is None:
            status = "only in doc1"
        else:
            response = llm_compare(field, val1, val2)

        if response:
            comparison_results[field] = {
                "doc1_value": val1,
                "doc2_value": val2,
                "status": response["status"],
                "confidence": response["confidence"],
                "reason": response["reason"],
            }
        else:
            comparison_results[field] = {
                "doc1_value": val1,
                "doc2_value": val2,
                "status": status,
            }

    return comparison_results

def save_comparison_results(results, output_file):
    """
    Save the comparison results to a JSON file.
    """
    import json
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def load_compare_and_save(doc1, doc2, output_file):
    """
    Compare two documents and save the results to a JSON file.
    """
    if os.path.exists(doc1) and os.path.exists(doc2):

        with open(doc1, 'r') as f1, open(doc2, 'r') as f2:
            doc1 = json.load(f1)
            doc2 = json.load(f2)
    results = compare_documents(doc1, doc2)
    save_comparison_results(results, output_file)

def compare_fields(extracted_paths: List[str], output_dir: str) -> str:
    """
    Compare documents in the extracted_paths and save the results to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, f"comparison_results.json")
    load_compare_and_save(extracted_paths[0], extracted_paths[1], output_file)
    print(f"Comparison results saved to {output_file}")

    return output_file

if __name__ == "__main__":
    compare_fields(["outputs/extracted/product_info_1.json", "outputs/extracted/product_info_2.json"], "outputs/comparisons")
