import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.metrotvnews.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

session = requests.Session()
session.headers.update(headers)

r = session.get(url, timeout=30)

print("Status:", r.status_code)
print("URL:", r.url)
print("HTML length:", len(r.text))

if r.status_code != 200:
    print("MetroTVNews blocked the GitHub Actions request.")
    print(r.text[:1000])
    raise SystemExit(1)

soup = BeautifulSoup(r.text, "html.parser")

results = []

# Find Most Popular widget on MetroTVNews
section = soup.find("section", class_="most-popular-2") or soup.find(
    "div", id="popular"
)

if section:
    # Find all popular items
    items = section.find_all("div", class_="popular-item")

    for item in items[:5]:
        a_tag = item.select_one("h3 a")
        date_tag = item.select_one(".date")

        if a_tag:
            title = a_tag.text.strip()
            link = a_tag.get("href", "").strip()
            date = date_tag.text.strip() if date_tag else ""

            results.append([title, link, date])

# Write findings to CSV
with open("popular.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "URL", "Date"])

    for row in results:
        writer.writerow(row)

print(f"Done. Found {len(results)} titles.")

for i, row in enumerate(results, 1):
    print(f"{i}. {row[0]} | {row[2]}")
