import requests
import csv
import re

url = "https://r.jina.ai/https://www.tempo.co/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Fetching Tempo.co...")

response = requests.get(
    url,
    headers=headers,
    timeout=60
)

response.raise_for_status()

text = response.text

print("Downloaded characters:", len(text))
print("ARTIKEL TRENDING found:", "ARTIKEL TRENDING" in text)

results = []
seen = set()

# Find ARTIKEL TRENDING section
match = re.search(
    r"ARTIKEL TRENDING(.*?)(?:ARTIKEL TERBARU|TOPIK TRENDING|$)",
    text,
    re.DOTALL | re.IGNORECASE
)

if match:
    section = match.group(1)

    # Find Markdown links inside the section
    links = re.findall(
        r"\[([^\]]+)\]\(([^)]+)\)",
        section
    )

    for title, link in links:
        title = " ".join(title.split()).strip()

        # Only Tempo article links
        if (
            title
            and "tempo.co/" in link
            and title not in seen
        ):
            seen.add(title)
            results.append([title])

# Stop if nothing was found.
# This prevents the old CSV from being overwritten.
if not results:
    print("ERROR: No trending titles found.")
    raise RuntimeError(
        "No ARTIKEL TRENDING titles found. "
        "popular.csv was NOT overwritten."
    )

# Save CSV
with open(
    "popular.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)
    writer.writerow(["Title"])
    writer.writerows(results)

print()
print(f"Done. Saved {len(results)} titles.")

for i, row in enumerate(results, start=1):
    print(f"{i}. {row[0]}")
