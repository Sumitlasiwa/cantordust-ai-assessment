import os
import json

def normalize(value):
    """
    Normalize the value for comparison according to the schema.
    """
    if isinstance(value, str):
        return value.strip().replace(" ", "").upper()
    elif isinstance(value, list):
        return [normalize(v) for v in value]
    else:
        return value

def compare_documents(doc1, doc2):
    """
    Compare two documents and return the comparison results.
    """
    schema_fields = set(doc1.keys()).union(set(doc2.keys()))

    comparison_results = {}

    for field in schema_fields:
        val1 = doc1.get(field)
        val2 = doc2.get(field)

        if normalize(val1) == normalize(val2):
            status = "match"
        elif val1 is None:
            status = "only in doc2"
        elif val2 is None:
            status = "only in doc1"
        else:
            status = "conflict"

        comparison_results[field] = {
            "doc1_value": val1,
            "doc2_value": val2,
            "status": status
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

def load_compare_and_save_through_directory(input_dir, output_dir):
    """
    Compare all pairs of documents in the input directory and save the results to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            doc1_path = os.path.join(input_dir, files[i])
            doc2_path = os.path.join(input_dir, files[j])
            output_file = os.path.join(output_dir, f"comparison_results.json")
            load_compare_and_save(doc1_path, doc2_path, output_file)

if __name__ == "__main__":
    load_compare_and_save_through_directory("outputs/extracted", "outputs/comparisons")
