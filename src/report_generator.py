# src/report_generator.py

import json
from pathlib import Path


def prettify(field_name: str) -> str:
    return field_name.replace("_", " ").title()


def generate_report(comparison_json_path: str, output_md_path: str):

    with open(comparison_json_path, "r", encoding="utf-8") as f:
        comparison = json.load(f)

    matches = []
    possible_matches = []
    conflicts = []
    only_doc1 = []
    only_doc2 = []

    for field, result in comparison.items():

        status = result.get("status", "").lower()

        if status == "match":
            matches.append((field, result))

        elif status == "possible match":
            possible_matches.append((field, result))

        elif status == "conflict":
            conflicts.append((field, result))

        elif status == "only in doc1":
            only_doc1.append((field, result))

        elif status == "only in doc2":
            only_doc2.append((field, result))

    report = []

    report.append("# SunBridge Import Review Draft\n")

    report.append(
        "This report compares manufacturer documents and highlights "
        "agreements, conflicts, and information requiring clarification.\n"
    )

    # Summary

    report.append("## Executive Summary\n")

    report.append(f"- Confirmed fields: {len(matches)}")
    report.append(f"- Possible matches: {len(possible_matches)}")
    report.append(f"- Conflicts: {len(conflicts)}")
    report.append(f"- Present only in Source 1: {len(only_doc1)}")
    report.append(f"- Present only in Source 2: {len(only_doc2)}\n")

    # Confirmed

    report.append("## Confirmed Specifications\n")

    if matches:
        report.append("| Field | Value |")
        report.append("|-------|-------|")

        for field, result in sorted(matches):
            value = result.get("doc1_value")
            report.append(
                f"| {prettify(field)} | {value} |"
            )

        report.append("")

    # Possible Matches

    report.append("## Possible Matches Requiring Review\n")

    if possible_matches:

        for field, result in sorted(possible_matches):

            report.append(f"### {prettify(field)}")

            report.append(
                f"- Source 1: {result.get('doc1_value')}"
            )

            report.append(
                f"- Source 2: {result.get('doc2_value')}"
            )

            if result.get("confidence") is not None:
                report.append(
                    f"- Confidence: {result['confidence']}"
                )

            if result.get("reason"):
                report.append(
                    f"- Reason: {result['reason']}"
                )

            report.append("")

    else:
        report.append("No possible matches detected.\n")

    # Conflicts

    report.append("## Conflicts Requiring Manufacturer Clarification\n")

    if conflicts:

        for field, result in sorted(conflicts):

            report.append(f"### {prettify(field)}")

            report.append(
                f"- Source 1: {result.get('doc1_value')}"
            )

            report.append(
                f"- Source 2: {result.get('doc2_value')}"
            )

            if result.get("reason"):
                report.append(
                    f"- Reason: {result['reason']}"
                )

            report.append("")

    else:
        report.append("No conflicts detected.\n")

    # Only in source 1

    report.append("## Information Present Only in Source 1\n")

    if only_doc1:

        report.append("| Field | Value |")
        report.append("|-------|-------|")

        for field, result in sorted(only_doc1):
            report.append(
                f"| {prettify(field)} | {result.get('doc1_value')} |"
            )

        report.append("")

    else:
        report.append("None.\n")

    # Only in source 2

    report.append("## Information Present Only in Source 2\n")

    if only_doc2:

        report.append("| Field | Value |")
        report.append("|-------|-------|")

        for field, result in sorted(only_doc2):
            report.append(
                f"| {prettify(field)} | {result.get('doc2_value')} |"
            )

        report.append("")

    else:
        report.append("None.\n")

    # Questions

    report.append("## Recommended Questions for Manufacturer\n")

    questions = []

    for field, result in conflicts + possible_matches:

        questions.append(
            f"- Please confirm the correct value for "
            f"'{prettify(field)}'. "
            f"Source 1 reports '{result.get('doc1_value')}' "
            f"while Source 2 reports '{result.get('doc2_value')}'."
        )

    if questions:
        report.extend(questions)
    else:
        report.append(
            "- No clarification questions required."
        )

    report.append("")

    Path(output_md_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"Report written to {output_md_path}")

if __name__ == "__main__":
    generate_report(
        comparison_json_path="outputs/comparisons/comparison_results.json",
        output_md_path="outputs/reports/final_report.md"
    )