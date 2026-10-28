from playwright.sync_api import Page, expect

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
