from tqdm import tqdm
from graph import graph
from graph_visualizer import save_graph_visualization

URLS = [
        "https://www.deyeinverter.com/deyeinverter/2023/10/07/datasheet_sun-4-12k-g06p3-eu-am2-p1_231007_en.pdf",
        "https://www.deyeinverter.com/deyeinverter/2024/03/20/datasheet_sun-4-15k-g06p3-eu-am2_240318_en.pdf"
    ]

final_report_path = "final_report.md"

with tqdm(total=5, desc="Pipeline", unit="step") as progress:
    for update in graph.stream(
        {"pdf_urls": URLS, "report_path": final_report_path},
        stream_mode="updates",
    ):
        completed_node = next(iter(update))
        progress.set_postfix(step=completed_node)
        progress.update(1)


print(f"✅ Report saved successfully to {final_report_path}")
save_graph_visualization()