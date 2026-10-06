import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.tempo.co/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

results = []

# Find ARTIKEL TRENDING heading
heading = soup.find(
    "span",
    string=lambda text: text and "ARTIKEL TRENDING" in text.strip()
)

if heading:

    # Find the parent section containing ARTIKEL TRENDING
    section = heading.find_parent("section")

    if section:

        # Titles are inside figcaption links
        headlines = section.select("figcaption p a")

        for h in headlines:
            title = h.get_text(" ", strip=True)

            if title:
                results.append([title])

# Write CSV (ONLY TITLES)
with open("popular.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["Title"])

    for row in results:
        writer.writerow(row)

print(f"Done. Saved popular.csv with {len(results)} titles.")
