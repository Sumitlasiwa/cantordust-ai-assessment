
import requests
from typing import List
import os

# Some hosts (e.g. the deyeinverter CDN) reject requests that lack a
# realistic User-Agent header. Using a common browser UA avoids 403s.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}


def fetch_pdf(url: str, dest: str) -> None:
    """Fetches a PDF from the given URL and saves it to the specified destination.
    """
    response = requests.get(url, headers=HEADERS, timeout=30)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(response.content)
        print(f"PDF downloaded successfully: {dest}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")

def fetch_pdfs_through_urls(urls: List[str], out_dir: str) -> None:
    """Fetches PDFs from a list of URLs and saves them to the specified output directory.
    """
    for i, url in enumerate(urls):
        dest = f"{out_dir}/datasheet_{i+1}.pdf"
        fetch_pdf(url, dest)
        
if __name__ == "__main__":

    URLS = [
        "https://www.deyeinverter.com/deyeinverter/2023/10/07/datasheet_sun-4-12k-g06p3-eu-am2-p1_231007_en.pdf",
        "https://www.deyeinverter.com/deyeinverter/2024/03/20/datasheet_sun-4-15k-g06p3-eu-am2_240318_en.pdf"
    ]
    fetch_pdfs_through_urls(URLS, "data/raw")
