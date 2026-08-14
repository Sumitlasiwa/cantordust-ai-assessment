# input: urls to pdf
# output: pdf files stored to specified directory

# Python example using requests
import requests
from typing import List

URLS = [
    "https://www.deyeinverter.com/deyeinverter/2023/10/07/datasheet_sun-4-12k-g06p3-eu-am2-p1_231007_en.pdf",
    "https://www.deyeinverter.com/deyeinverter/2024/03/20/datasheet_sun-4-15k-g06p3-eu-am2_240318_en.pdf"
]

# Some hosts (e.g. the deyeinverter CDN) reject requests that lack a
# realistic User-Agent header. Using a common browser UA avoids 403s.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
}

OUT_DIR = "data/raw"


def fetch_pdf(url: str, dest: str) -> None:
    response = requests.get(url, headers=HEADERS, timeout=30)
    if response.status_code == 200:
        with open(dest, "wb") as f:
            f.write(response.content)
        print(f"PDF downloaded successfully: {dest}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")


if __name__ == "__main__":
    for i, url in enumerate(URLS):
        fetch_pdf(url, f"{OUT_DIR}/datasheet_{i+1}.pdf")  

