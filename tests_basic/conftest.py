import pytest
from playwright.sync_api import Page


@pytest.fixture
def practice_page(page: Page):
    """
    Prepara la página de prácticas para los tests.

    Reutiliza la fixture 'page' de pytest-playwright y navega
    a la URL configurada en el proyecto.
    """

    # SETUP: prepara la página antes de ejecutar el test.
    print("\n>>> SETUP")
    page.goto("/practice.html")

    # Entrega la página al test y pausa la fixture hasta que termine.
    yield page

    # TEARDOWN: se ejecuta al finalizar el test, incluso si falla.
    print("\n>>> TEARDOWN")