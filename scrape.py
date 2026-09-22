import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cnbcindonesia.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

results = []

# Find CNBC Indonesia Most Popular widget
section = soup.find(
    "div",
    attrs={
        "data-name": "widget",
        "data-target": "wp_terpopuler"
    }
)

if section:
    # Find all links belonging to the popular widget
    headlines = section.find_all("a", attrs={"dtr-evt": "box terpopuler"})

    for a in headlines:
        title = a.get("dtr-ttl", "").strip()

        if title:
            results.append([title])

# Only keep first 5
results = results[:5]

# Write CSV
with open("popular.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title"])

    for row in results:
        writer.writerow(row)

print(f"Done. Found {len(results)} titles.")

for i, row in enumerate(results, 1):
    print(f"{i}. {row[0]}")
