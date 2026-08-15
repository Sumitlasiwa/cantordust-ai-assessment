from graph import graph

URLS = [
        "https://www.deyeinverter.com/deyeinverter/2023/10/07/datasheet_sun-4-12k-g06p3-eu-am2-p1_231007_en.pdf",
        "https://www.deyeinverter.com/deyeinverter/2024/03/20/datasheet_sun-4-15k-g06p3-eu-am2_240318_en.pdf"
    ]

final_report_path = "outputs/reports/final_report.md"

graph.invoke({"pdf_urls": URLS, "report_path": final_report_path})