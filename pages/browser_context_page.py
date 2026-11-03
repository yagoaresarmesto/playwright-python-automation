from playwright.sync_api import Page


class BrowserContextPage:
    """
    Page Object del Módulo 6 — Browser Context, Tabs & Windows.

    Centraliza los locators y las acciones de la página.
    Las assertions se realizan en los tests.
    """

    def __init__(self, page: Page):
        self.page = page

        # Botón que abre una nueva pestaña.
        self.open_tab_button = page.get_by_test_id("btn-open-pw-tab")

        # Botón que abre una nueva ventana.
        self.open_window_button = page.get_by_test_id("btn-open-mw-window")

    def click_open_tab(self):
        # Pulsamos el botón que abre una nueva pestaña.
        self.open_tab_button.click()

    def click_open_window(self):
        self.open_window_button.click()