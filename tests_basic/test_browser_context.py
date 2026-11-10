"""Módulo 6 — Browser Context, Tabs & Windows."""

from playwright.sync_api import Browser, Page, expect

from pages.browser_context_page import BrowserContextPage


# --- Pestañas y páginas del contexto ---

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


# --- Pestañas abiertas mediante eventos ---

# Ejercicio 50 — Capturar una pestaña abierta mediante un clic.
def test_open_tab_by_click(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with context.expect_page() as new_page_info:
        browser_context_page.click_open_tab()

    new_page = new_page_info.value

    assert not new_page.is_closed()
    expect(new_page).to_have_url("https://playwright.dev/")


# --- Ventanas emergentes (popups) ---

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


# --- Interacción entre pestañas ---

# Ejercicio 58 — Interactuar con una segunda pestaña.
def test_interact_with_new_tab(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with context.expect_page() as new_page_info:
        browser_context_page.click_open_tab()

    new_page = new_page_info.value

    expect(new_page).to_have_url("https://playwright.dev/")

    get_started_link = new_page.get_by_role("link", name="Get started")

    expect(get_started_link).to_be_visible()


# Ejercicio 59 — Navegar desde una segunda pestaña.
def test_navigate_from_new_tab(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with context.expect_page() as new_page_info:
        browser_context_page.click_open_tab()

    new_page = new_page_info.value

    expect(new_page).to_have_url("https://playwright.dev/")

    get_started_link = new_page.get_by_role("link", name="Get started")

    expect(get_started_link).to_be_visible()

    get_started_link.click()

    expect(new_page).to_have_url("https://playwright.dev/docs/intro")


# Ejercicio 60 — Interactuar con la página original tras cerrar otra pestaña.
def test_return_to_original_page(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)
    context = practice_page.context

    with context.expect_page() as new_page_info:
        browser_context_page.click_open_tab()

    new_page = new_page_info.value

    expect(new_page).to_have_url("https://playwright.dev/")

    new_page.close()

    assert not practice_page.is_closed()

    with context.expect_page() as second_tab_info:
        browser_context_page.click_open_tab()

    second_tab = second_tab_info.value

    expect(second_tab).to_have_url("https://playwright.dev/")

    assert not practice_page.is_closed()


# Ejercicio 61 — Comprobar el contexto de una nueva pestaña.
def test_new_tab_shares_context(practice_page: Page):
    browser_context_page = BrowserContextPage(practice_page)

    with practice_page.context.expect_page() as new_page_info:
        browser_context_page.click_open_tab()

    new_page = new_page_info.value

    assert practice_page.context is new_page.context


# --- Aislamiento entre contextos ---

# Ejercicio 62 — Comprobar que dos contextos son independientes.
def test_independent_contexts(browser: Browser):
    context_a = browser.new_context()
    context_b = browser.new_context()

    page_a = context_a.new_page()
    page_b = context_b.new_page()

    try:
        assert page_a.context is not page_b.context
    finally:
        context_a.close()
        context_b.close()


# Ejercicio 63 — Comprobar el aislamiento de páginas entre contextos.
def test_pages_are_isolated_between_contexts(browser: Browser):
    context_a = browser.new_context()
    context_b = browser.new_context()

    page_a = context_a.new_page()
    page_b = context_b.new_page()

    try:
        assert page_a in context_a.pages
        assert page_a not in context_b.pages
        assert page_b in context_b.pages

    finally:
        context_a.close()
        context_b.close()


# --- Cookies ---

# Ejercicio 64 — Comprobar el aislamiento de cookies.
def test_cookies_are_isolated_between_contexts(browser: Browser):
    context_a = browser.new_context()
    context_b = browser.new_context()

    try:
        context_a.add_cookies([
            {
                "name": "usuario",
                "value": "QA_Automation",
                "url": "https://example.com",
            }
        ])

        cookies_a = context_a.cookies()
        cookies_b = context_b.cookies()

        assert cookies_a[0]["name"] == "usuario"
        assert cookies_a[0]["value"] == "QA_Automation"
        assert cookies_b == []

    finally:
        context_a.close()
        context_b.close()


# Ejercicio 65 — Eliminar cookies de un contexto.
def test_clear_context_cookies(browser: Browser):
    context = browser.new_context()

    try:
        context.add_cookies([
            {
                "name": "usuario",
                "value": "QA_Automation",
                "url": "https://example.com",
            }
        ])
        assert len(context.cookies()) == 1
        context.clear_cookies()
        assert context.cookies() == []

    finally:
        context.close()


# --- Storage State ---

# Ejercicio 66 — Inspeccionar el Storage State.
def test_inspect_storage_state(browser: Browser):
    context = browser.new_context()

    try:
        context.add_cookies([
            {
                "name": "usuario",
                "value": "QA_Automation",
                "url": "https://example.com",
            }
        ])
        state = context.storage_state()
        print(state)
        assert state["cookies"][0]["value"] == "QA_Automation"

    finally:
         context.close()


# Ejercicio 67 — Guardar el Storage State en JSON.
def test_save_storage_state(browser: Browser):
    context = browser.new_context()

    try:
        context.add_cookies([
            {
                "name": "usuario",
                "value": "QA_Automation",
                "url": "https://example.com",
            }
        ])
        context.storage_state(path="storage_state.json")

    finally:
         context.close()


# Ejercicio 68 — Cargar el Storage State desde JSON.
def test_load_storage_state(browser: Browser):
    context = browser.new_context(storage_state="storage_state.json")

    try:
        cookies = context.cookies()
        assert cookies[0]["name"] == "usuario"
        assert cookies[0]["value"] == "QA_Automation"

    finally:
         context.close()


# Ejercicio 69 — Comprobar el aislamiento al cargar Storage State.
def test_storage_state_isolated_between_contexts(browser: Browser):
    context_a = browser.new_context(storage_state="storage_state.json")
    context_b = browser.new_context()

    try:
        cookies_a = context_a.cookies()
        cookies_b = context_b.cookies()

        assert cookies_a[0]["name"] == "usuario"
        assert cookies_a[0]["value"] == "QA_Automation"
        assert cookies_b == []

    finally:
        context_a.close()
        context_b.close()


# Ejercicio 70 — Recuperar una sesión después de limpiar cookies.
def test_restore_cookies_after_clearing_context(browser: Browser):
    context_a = browser.new_context(storage_state="storage_state.json")
    context_b = browser.new_context(storage_state="storage_state.json")

    try:
        cookies_a = context_a.cookies()
        assert cookies_a[0]["name"] == "usuario"
        context_a.clear_cookies()
        assert context_a.cookies() == []

        cookies_b = context_b.cookies()
        assert cookies_b[0]["name"] == "usuario"
        assert cookies_b[0]["value"] == "QA_Automation"

    finally:
        context_a.close()
        context_b.close()