from playwright.sync_api import Page, expect
from pages.tables_page import TablesPage
import pytest

# MODULE 4 — Tables | Static Web Table — Primera fila
# Comprueba que la tabla y su primera fila están visibles,
# y que el total de medallas de USA es 22.
def test_static_table_first_row(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Verificamos que la tabla está visible en la página.
    expect(tables_page.static_table).to_be_visible()

    # Comprobamos que la primera fila de datos está visible.
    expect(tables_page.static_first_row).to_be_visible()

    # Verificamos que la sexta celda de la primera fila contiene "22".
    expect(tables_page.static_usa_total).to_have_text("22")

# MODULE 4 — Tables | Static Web Table — Buscar fila por contenido
# Comprueba que podemos localizar la fila de USA sin depender de su posición.
def test_static_table_usa_row(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Buscamos dentro de la tabla estática una fila de datos
    # que contenga el texto "USA", independientemente de su posición.
    usa_row = tables_page.static_table.locator(
        "tbody tr",
        has_text="USA"
    )

    # Verificamos que la fila encontrada está visible.
    expect(usa_row).to_be_visible()

    # Comprobamos que la fila contiene el deporte "Swimming".
    expect(usa_row).to_contain_text("Swimming")

# MODULE 4 — Tables | Static Web Table — Total de medallas de USA
# Comprueba el total de medallas sin depender de la posición de la fila.
def test_static_table_usa_total_medals(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Buscamos la fila que contiene "USA" dentro de la tabla estática.
    # No importa si USA aparece en la primera, segunda o cuarta fila.
    usa_row = tables_page.static_table.locator(
        "tbody tr",
        has_text="USA"
    )

    # Localizamos todas las celdas <td> de la fila de USA.
    # nth(5) selecciona la sexta celda porque los índices empiezan en 0.
    # En esta tabla, esa celda corresponde a Total Medals.
    medals_usa = usa_row.locator("td").nth(5)

    # Verificamos que el total de medallas de USA es exactamente 22.
    expect(medals_usa).to_have_text("22")

# MODULE 4 — Tables | Static Web Table — Suma de medallas
# Comprueba que la suma de oro, plata y bronce coincide
# con el total de medallas de USA.
def test_static_table_usa_medals_sum(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Localizamos la fila de USA sin depender de su posición.
    usa_row = tables_page.static_table.locator(
        "tbody tr",
        has_text="USA"
    )

    # Leemos el texto de cada celda con inner_text().
    # Convertimos directamente cada resultado de str a int.
    gold = int(usa_row.locator("td").nth(2).inner_text())
    silver = int(usa_row.locator("td").nth(3).inner_text())
    bronze = int(usa_row.locator("td").nth(4).inner_text())
    total = int(usa_row.locator("td").nth(5).inner_text())

    # Verificamos que la suma coincide con el total indicado.
    assert gold + silver + bronze == total

# MODULE 4 — Tables | Static Web Table — Suma de medallas parametrizada
# Ejecuta la misma comprobación para USA, China e India sin duplicar tests.
@pytest.mark.parametrize("country", ["USA", "China", "India"])
def test_static_table_medals_sum_parametrized(practice_page: Page, country):
    tables_page = TablesPage(practice_page)

    # Localizamos la fila del país recibido como parámetro.
    # has_text=country permite buscar un país diferente en cada ejecución.
    country_row = tables_page.static_table.locator(
        "tbody tr",
        has_text=country
    )

    # Obtenemos el texto de las celdas y lo convertimos directamente
    # a números enteros para poder realizar operaciones matemáticas.
    gold = int(country_row.locator("td").nth(2).inner_text())
    silver = int(country_row.locator("td").nth(3).inner_text())
    bronze = int(country_row.locator("td").nth(4).inner_text())
    total = int(country_row.locator("td").nth(5).inner_text())

    # Verificamos que la suma de oro, plata y bronce coincide
    # con el total de medallas indicado para cada país.
    # Podemos hacer que la assertion indique qué país tiene el problema
    assert gold + silver + bronze == total, (
        f"{country}: la suma es {gold + silver + bronze}, "
        f"pero el total indicado es {total}."
    )

# MODULE 4 — Tables | Static Web Table — Validar todas las filas
# Comprueba automáticamente que la suma de medallas coincide
# con el total indicado para todos los países de la tabla.
def test_static_table_all_medals_sum(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Localizamos todas las filas de datos de la tabla estática.
    rows = tables_page.static_table.locator("tbody tr")

    # Obtenemos el número total de filas.
    total_rows = rows.count()

    # Comprobamos que la tabla contiene al menos una fila.
    assert total_rows > 0

    # Recorremos todas las filas, una por una.
    for i in range(total_rows):

        # Seleccionamos la fila actual según su índice.
        row = rows.nth(i)

        # Obtenemos el nombre del país para identificarlo
        # en caso de que falle la comprobación.
        cells = row.locator("td")
        country = cells.nth(0).inner_text()

        # Extraemos las medallas y convertimos el texto a enteros.
        gold = int(cells.nth(2).inner_text())
        silver = int(cells.nth(3).inner_text())
        bronze = int(cells.nth(4).inner_text())
        total = int(cells.nth(5).inner_text())

        # Verificamos la suma de medallas para el país actual.
        assert gold + silver + bronze == total, (
            f"{country}: la suma es {gold + silver + bronze}, "
            f"pero el total indicado es {total}."
        )

# MODULE 4 — Tables | Dynamic Table — Comprobar filas
# Verifica que la tabla dinámica está visible y contiene datos.
def test_dynamic_table_has_rows(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Comprobamos que la tabla dinámica está visible.
    expect(tables_page.dynamic_table).to_be_visible()

    # Localizamos las filas dentro del cuerpo de la tabla.
    rows = tables_page.dynamic_table_body.locator("tr")

    # Esperamos a que aparezca al menos una fila visible.
    expect(rows.first).to_be_visible()


# MODULE 4 — Tables | Dynamic Table — Localizar un club
# Comprueba que Barcelona aparece en una celda de la tabla dinámica,
# sin depender de la posición de la fila ni de la columna.
def test_dynamic_table_barcelona(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Localizamos la fila que contiene el nombre Barcelona.
    barcelona_row = tables_page.dynamic_table_body.locator(
        "tr",
        has_text="Barcelona"
    )

    # Comprobamos que la fila está visible.
    expect(barcelona_row).to_be_visible()

    # Localizamos la celda que contiene Barcelona dentro de esa fila.
    # No necesitamos saber qué posición ocupa.
    barcelona_cell = barcelona_row.locator(
        "td",
        has_text="Barcelona"
    )

    # Verificamos que la celda contiene exactamente Barcelona.
    expect(barcelona_cell).to_have_text("Barcelona")

# MODULE 4 — Tables | Dynamic Table — Localizar columna por encabezado
# Comprueba que existe la columna Goals y obtiene su posición.
def test_dynamic_table_goals_header(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Localizamos todos los encabezados de la tabla dinámica.
    headers = tables_page.dynamic_table.locator("thead th")

    # Obtenemos sus textos en una lista de Python.
    header_texts = headers.all_inner_texts()

    print("Encabezados:", header_texts)

    # Buscamos la posición de Goals dentro de la lista.
    # Si no existe, index() lanzará un ValueError.
    goals_index = header_texts.index("Goals")

    print("Índice de Goals:", goals_index)

    # El índice 0 también es válido: representa la primera columna.
    assert goals_index >= 0

# MODULE 4 — Tables | Dynamic Table — Validar goles de Barcelona
# Comprueba que los goles de Barcelona son un número entero
# mayor o igual que cero, sin depender del orden de las columnas.
def test_dynamic_table_barcelona_goals(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Buscamos la posición de la columna GOALS.
    goals_index = tables_page.get_dynamic_column_index("GOALS")

    # Buscamos la fila de Barcelona.
    barcelona_row = tables_page.get_dynamic_club_row("Barcelona")

    # Comprobamos que la fila esté visible.
    expect(barcelona_row).to_be_visible()

    # Obtenemos todas las celdas de Barcelona.
    cells = barcelona_row.locator("td")

    # Leemos los goles y los convertimos a entero.
    barcelona_goals = int(cells.nth(goals_index).inner_text())

    # Comprobamos que los goles no sean negativos.
    assert barcelona_goals >= 0

def test_dynamic_table_barcelona_goals_and_points(practice_page: Page):
    tables_page = TablesPage(practice_page)

    # Obtenemos la posición actual de ambas columnas.
    goals_index = tables_page.get_dynamic_column_index("GOALS")
    points_index = tables_page.get_dynamic_column_index("POINTS")

    # Localizamos la fila de Barcelona.
    barcelona_row = tables_page.get_dynamic_club_row("Barcelona")

    # Comprobamos que la fila esté visible.
    expect(barcelona_row).to_be_visible()

    # Obtenemos sus celdas.
    cells = barcelona_row.locator("td")

    # Leemos goles y puntos como números enteros.
    barcelona_goals = int(cells.nth(goals_index).inner_text())
    barcelona_points = int(cells.nth(points_index).inner_text())

    # Validamos ambos valores por separado.
    assert barcelona_goals >= 0
    assert barcelona_points >= 0