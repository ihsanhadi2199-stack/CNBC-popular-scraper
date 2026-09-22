import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.metrotvnews.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
}

session = requests.Session()
session.headers.update(headers)

r = session.get(url, timeout=30)
soup = BeautifulSoup(r.text, "html.parser")

results = []

# Select popular items directly across the page
items = soup.select(".popular-item")

for item in items[:5]:
    a_tag = item.select_one("h3 a") or item.select_one("a")
    date_tag = item.select_one(".date")

    if a_tag:
        title = a_tag.text.strip() or a_tag.get("title", "").strip()
        link = a_tag.get("href", "").strip()
        date = date_tag.text.strip() if date_tag else ""

        if title:
            results.append([title, link, date])

# Write findings to CSV
with open("popular.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "URL", "Date"])
    writer.writerows(results)

print(f"Done. Found {len(results)} titles.")
for i, row in enumerate(results, 1):
    print(f"{i}. {row[0]}")
