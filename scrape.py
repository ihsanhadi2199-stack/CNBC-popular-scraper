import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.cnbcindonesia.com/"

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
    print("CNBC blocked the GitHub Actions request.")
    print(r.text[:1000])
    raise SystemExit(1)

soup = BeautifulSoup(r.text, "html.parser")

results = []

# Find Most Popular widget
section = soup.find(
    "div",
    attrs={
        "data-name": "widget",
        "data-target": "wp_terpopuler"
    }
)

if section:
    # CNBC puts the title in dtr-ttl
    headlines = section.find_all(
        "a",
        attrs={"dtr-evt": "box terpopuler"}
    )

    for a in headlines[:5]:
        title = a.get("dtr-ttl", "").strip()

        if title:
            results.append([title])

with open("popular.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title"])

    for row in results:
        writer.writerow(row)

print(f"Done. Found {len(results)} titles.")

for i, row in enumerate(results, 1):
    print(f"{i}. {row[0]}")
