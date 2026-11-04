"""Módulo 6 — Browser Context, Tabs & Windows."""

from playwright.sync_api import Page, expect

from pages.browser_context_page import BrowserContextPage


# Ejercicio 45 — Abrir una segunda pestaña y validar su título.
def test_open_new_tab(practice_page: Page):
    context = practice_page.context
    new_page = context.new_page()

    new_page.goto("https://example.com")
    expect(new_page).to_have_title("Example Domain")


# Ejercicio 46 — Comprobar el número de pestañas abiertas.
def test_context_has_two_pages(practice_page: Page):
    context = practice_page.context
    new_page = context.new_page()

    assert len(context.pages) == 2


# Ejercicios 47 y 48 — Cerrar una pestaña e identificar la restante.
def test_close_new_tab(practice_page: Page):
    context = practice_page.context
    new_page = context.new_page()

    assert len(context.pages) == 2

    new_page.close()

    assert len(context.pages) == 1
    assert context.pages[0] == practice_page


# Ejercicio 49 — Comprobar que la página original sigue abierta.
def test_work_with_two_tabs(practice_page: Page):
    context = practice_page.context
    new_page = context.new_page()

    new_page.goto("https://example.com")
    expect(new_page).to_have_title("Example Domain")
    assert not practice_page.is_closed()


# Ejercicio 50 — Capturar una pestaña abierta mediante un clic.
def test_open_tab_by_click(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with context.expect_page() as new_page_info:
        browser_context_page.click_open_tab()

    new_page = new_page_info.value

    assert not new_page.is_closed()
    expect(new_page).to_have_url("https://playwright.dev/")


# Ejercicio 51 — Capturar una ventana emergente (popup).
def test_open_popup_window(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value
    assert not popup.is_closed()


# Ejercicio 53 — Validar la URL del popup.
# El ejercicio 52 fue exploratorio: imprimir la URL para descubrir su destino.
def test_popup_url(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value
    expect(popup).to_have_url("https://mobilewright.dev/")


# Ejercicio 54 — Cerrar el popup sin cerrar la página original.
def test_close_popup_window(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value
    popup.close()

    assert popup.is_closed()
    assert not practice_page.is_closed()


# Ejercicio 55 — Contar páginas antes y después de cerrar el popup.
def test_popup_pages_count(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value
    assert len(context.pages) == 2

    popup.close()
    assert len(context.pages) == 1


# Ejercicio 56 — Validar la página original y el popup por separado.
def test_original_page_and_popup(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value

    expect(popup).to_have_url("https://mobilewright.dev/")
    expect(practice_page).to_have_url(
        "https://www.playwrightautomation.com/practice.html"
    )

    popup.close()
    assert not practice_page.is_closed()


# Ejercicio 57 — Confirmar que la página original permanece en el contexto.
def test_original_page_remains_in_context(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value
    assert len(context.pages) == 2

    popup.close()

    assert len(context.pages) == 1
    assert practice_page in context.pages