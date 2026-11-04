from playwright.sync_api import Page, expect
from pages.browser_context_page import BrowserContextPage

# MODULE 6 — Browser Context, Tabs & Windows
#Abrir una segunda pestaña.

def test_open_new_tab(practice_page: Page):
    # Obtenemos el contexto de la página actual.
    context = practice_page.context

    # Abrimos una segunda pestaña en el mismo contexto.
    new_page = context.new_page()

    new_page.goto("https://example.com")
    expect(new_page).to_have_title("Example Domain")

# MODULE 6 — Browser Context, Tabs & Windows
# Ejercicio 46 — Comprobar el número de pestañas.
def test_context_has_two_pages(practice_page: Page):
    context = practice_page.context

    # Abrimos una segunda pestaña.
    new_page = context.new_page()

    # Comprobamos que existen dos pestañas en el contexto.
    assert len(context.pages) == 2

# MODULE 6 — Browser Context, Tabs & Windows
# Cerrar una pestaña.
def test_close_new_tab(practice_page: Page):
    context = practice_page.context

    # Abrimos una segunda pestaña.
    new_page = context.new_page()

    # Comprobamos que hay dos pestañas.
    assert len(context.pages) == 2

    # Cerramos la segunda pestaña.
    new_page.close()

    #Comprobar que ahora solo queda una pestaña.
    assert len(context.pages) == 1

    #Comprobar que la pestaña restante es practice_page.
    assert context.pages[0] == practice_page

# MODULE 6 — Browser Context, Tabs & Windows
# Trabajar con dos pestañas.
def test_work_with_two_tabs(practice_page: Page):
    context = practice_page.context

    # Abrimos una segunda pestaña.
    new_page = context.new_page()

    # Navegar a https://example.com
    new_page.goto("https://example.com")

    # Comprobar que el título es "Example Domain"
    expect(new_page).to_have_title("Example Domain")

    # Comprobar que practice_page sigue abierta.
    assert not practice_page.is_closed()

# MODULE 6 — Browser Context, Tabs & Windows
# Ejercicio 50 — Capturar una pestaña abierta mediante un clic.
def test_open_tab_by_click(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    # Obtenemos el contexto de la página actual.
    context = practice_page.context

    # Esperamos una nueva pestaña y hacemos clic.
    with context.expect_page() as new_page_info:
        browser_context_page.click_open_tab()

    # Recuperamos la pestaña después de finalizar la espera.
    new_page = new_page_info.value

    # Comprobamos que la nueva pestaña está abierta.
    assert not new_page.is_closed()

    # Comprobamos que hemos llegado a la documentación de Playwright.
    expect(new_page).to_have_url("https://playwright.dev/")

# MODULE 6 — Browser Context, Tabs & Windows
def test_open_popup_window(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    # Esperamos a que la página original abra un popup.
    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    # Recuperamos la ventana emergente.
    popup = popup_info.value

    # Comprobamos que sigue abierta.
    assert not popup.is_closed()

# MODULE 6 — Browser Context, Tabs & Windows
def test_popup_url(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    # Esperamos a que la página original abra un popup.
    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    # Recuperamos la ventana emergente.
    popup = popup_info.value

    # Comprobamos que el popup abre la URL esperada.


def test_close_popup_window(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value

    popup.close()

    assert popup.is_closed()

    assert not practice_page.is_closed()

def test_popup_pages_count(practice_page: Page):

    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value

    assert len(context.pages) == 2

    popup.close()

    assert len(context.pages) == 1

def test_original_page_and_popup(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    with practice_page.expect_popup() as popup_info:
        browser_context_page.click_open_window()

    popup = popup_info.value

    expect(popup).to_have_url("https://mobilewright.dev/")
    expect(practice_page).to_have_url("https://www.playwrightautomation.com/practice.html")

    popup.close()

    assert not practice_page.is_closed()

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

