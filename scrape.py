from playwright.sync_api import sync_playwright

url = "https://www.tempo.co/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        )
    )

    response = page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("HTTP status:", response.status if response else "No response")
    print("Final URL:", page.url)
    print("Page title:", page.title())

    html = page.content()

    print("HTML length:", len(html))
    print("Contains ARTIKEL TRENDING:", "ARTIKEL TRENDING" in html)

    # Save whatever GitHub Actions actually received
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    page.screenshot(path="debug.png", full_page=True)

    browser.close()
