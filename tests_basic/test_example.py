from playwright.sync_api import sync_playwright


def test_open_example():
    with sync_playwright() as p: #Inicia playwright p nos da acceso a los motores del navegador
        browser = p.chromium.launch(
            channel="msedge", #Nuestro caso chromium + edge
            headless=False #Muestrame el navegador, pero más adelante se suele poner a True
        )

        context = browser.new_context()
        page = context.new_page()

        page.goto("https://example.com")

        assert "Example Domain" in page.title()

        browser.close()