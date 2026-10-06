from playwright.sync_api import sync_playwright
import csv

url = "https://www.tempo.co/"

results = []
seen = set()

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        locale="id-ID",
        viewport={
            "width": 1920,
            "height": 1080
        }
    )

    page = context.new_page()

    print("Opening Tempo.co...")

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    # Wait until ARTIKEL TRENDING is rendered by JavaScript
    try:
        page.get_by_text(
            "ARTIKEL TRENDING",
            exact=True
        ).wait_for(timeout=30000)

    except Exception:
        browser.close()
        raise RuntimeError(
            "ARTIKEL TRENDING section was not found."
        )

    # Locate the heading
    heading = page.get_by_text(
        "ARTIKEL TRENDING",
        exact=True
    ).first

    # Get the section containing the heading
    section = heading.locator(
        "xpath=ancestor::section[1]"
    )

    # Get article titles only
    headlines = section.locator(
        "figcaption p a"
    )

    count = headlines.count()

    print(f"Found {count} headline elements.")

    for i in range(count):

        title = headlines.nth(i).inner_text().strip()

        # Normalize whitespace
        title = " ".join(title.split())

        if title and title not in seen:
            seen.add(title)
            results.append([title])

    browser.close()


# IMPORTANT:
# Do not overwrite existing CSV if scraping failed
if not results:
    raise RuntimeError(
        "No Tempo trending titles were found. "
        "popular.csv was NOT overwritten."
    )


# Write CSV
with open(
    "popular.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow(["Title"])

    for row in results:
        writer.writerow(row)


print(
    f"Done. Saved popular.csv with "
    f"{len(results)} titles."
)

for number, row in enumerate(results, start=1):
    print(f"{number}. {row[0]}")
