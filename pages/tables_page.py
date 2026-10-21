from playwright.sync_api import Page


class TablesPage:
    """
    Page Object del Módulo 4 — Tables.

    Centraliza los locators y las acciones de las tablas.
    Las assertions se realizan en los tests.
    """

    def __init__(self, page: Page):
        self.page = page

        self.static_table = page.get_by_test_id("static-table")
        self.static_first_row = page.get_by_test_id("static-row-1")
        self.static_usa_total = page.get_by_test_id("static-cell-1-6")

        # Dynamic Table
        self.dynamic_table = page.get_by_test_id("table-dynamic")
        self.dynamic_table_body = page.locator("#dynamic-table-body")

    def get_dynamic_column_index(self, column_name: str) -> int:
        # Obtenemos todos los encabezados.
        headers = self.dynamic_table.locator("thead th")

        # Convertimos sus textos en una lista.
        header_texts = headers.all_inner_texts()

        # Devolvemos la posición del encabezado solicitado.
        return header_texts.index(column_name)

    def get_dynamic_club_row(self, club_name: str):
        # Localizamos la fila que contiene el nombre del club.
        club_row = self.dynamic_table_body.locator(
            "tr",
            has_text=club_name
        )
        # Devolvemos el Locator, no el texto de la fila.
        return club_row