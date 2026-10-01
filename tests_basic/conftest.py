import pytest
from playwright.sync_api import Page


@pytest.fixture
def practice_page(page: Page):
    print("\n>>> SETUP")
    page.goto("/practice.html")

    yield page

    print("\n>>> TEARDOWN")

