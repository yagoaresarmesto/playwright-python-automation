from playwright.sync_api import Page


class BrowserContextPage:
    """
    Page Object del Módulo 6 — Browser Context, Tabs & Windows.

    Contiene los locators y las acciones necesarias para abrir
    nuevas pestañas y ventanas desde la página de prácticas.
    """

    def __init__(self, page: Page):
        self.page = page

        # Locators — Browser Context, Tabs & Windows
        self.open_tab_button = page.get_by_test_id("btn-open-pw-tab")
        self.open_window_button = page.get_by_test_id("btn-open-mw-window")

    # Actions
    def click_open_tab(self):
        self.open_tab_button.click()

    def click_open_window(self):
        self.open_window_button.click()