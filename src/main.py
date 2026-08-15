from fetcher import fetch_pdfs_through_urls as download_pdf
from parser import extract_text_from_pdfs_through_directory as extract_text
from extractor import extract_and_save_product_info_through_directory as extract_fields
from comparator import load_compare_and_save_through_directory as compare_fields
from report_generator import generate_report


URLS = [
        "https://www.deyeinverter.com/deyeinverter/2023/10/07/datasheet_sun-4-12k-g06p3-eu-am2-p1_231007_en.pdf",
        "https://www.deyeinverter.com/deyeinverter/2024/03/20/datasheet_sun-4-15k-g06p3-eu-am2_240318_en.pdf"
    ]

final_report_path = "outputs/reports/final_report.md"

download_pdf(urls=URLS, out_dir="data/raw")
extract_text(input_dir="data/raw", output_dir="data/processed")
extract_fields(input_dir="data/processed", output_dir="outputs/extracted")
compare_fields(input_dir="outputs/extracted", output_dir="outputs/comparisons")
generate_report(comparison_json_path="outputs/comparisons/comparison_results.json", output_md_path=final_report_path)