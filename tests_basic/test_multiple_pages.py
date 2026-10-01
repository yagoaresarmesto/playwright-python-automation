from playwright.sync_api import sync_playwright


def test_multiple_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel = "msedge", headless=False)

        context = browser.new_context()

        page1 = context.new_page()
        page2 = context.new_page()

        page1.goto("https://example.com")
        page2.goto("https://www.python.org")

        page1.wait_for_timeout(5000)

        browser.close()