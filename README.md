# PlaywrightAutomation

Proyecto de **aprendizaje y práctica de automatización de pruebas web** con **Python, Playwright y pytest**, organizado mediante el patrón **Page Object Model (POM)**.

El objetivo es practicar la localización de elementos, la interacción con páginas web, las comprobaciones automáticas (`assert` y `expect`) y la gestión del navegador. Los tests utilizan la página de prácticas de [Playwright Automation](https://www.playwrightautomation.com/practice.html).

## Tecnologías

- **Python**: lenguaje de programación.
- **Playwright**: automatización del navegador.
- **pytest** y **pytest-playwright**: ejecución de tests y fixtures.
- **Microsoft Edge**: navegador configurado para ejecutar las pruebas.
- **Page Object Model (POM)**: separación de locators y acciones respecto a las comprobaciones de los tests.

## Contenido del proyecto

| Módulo | Archivo de tests | Qué se practica |
| --- | --- | --- |
| Controles de formularios | `test_form_controls.py` | Campos, validaciones, interruptores, mostrar/ocultar elementos, selección múltiple, tooltips y contenido AJAX. |
| Alertas de JavaScript | `test_javascript_alerts.py` | Diálogos `alert`, `confirm` y `prompt`; aceptar, cancelar e introducir texto. |
| Gestión de archivos | `test_file_handling.py` | Subida de uno o varios archivos y restablecimiento de la selección. |
| Tablas | `test_tables.py` | Tablas estáticas y dinámicas, filas, columnas y comprobaciones de valores; tests parametrizados. |
| Browser Context, Tabs & Windows | `test_browser_context.py` | Pestañas, popups, contextos independientes, cookies y almacenamiento de sesión (`storage_state`). |

El proyecto contiene **62 tests** en los cinco archivos de pruebas incluidos en la copia revisada. Esta cifra puede cambiar a medida que se añadan o modifiquen pruebas.

## Estructura

```text
PlaywrightAutomation/
├── pages/
│   ├── browser_context_page.py
│   ├── file_handling_page.py
│   ├── form_controls_page.py
│   ├── javascript_alerts_page.py
│   └── tables_page.py
├── tests_basic/
│   ├── conftest.py
│   ├── test_browser_context.py
│   ├── test_file_handling.py
│   ├── test_form_controls.py
│   ├── test_javascript_alerts.py
│   └── test_tables.py
├── docs/
│   └── debugging.md
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

- **`pages/`**: clases POM con los locators y las acciones reutilizables.
- **`tests_basic/`**: escenarios de prueba y sus assertions.
- **`tests_basic/conftest.py`**: fixture `practice_page`, que abre la página de prácticas antes de cada test que la solicita.
- **`docs/debugging.md`**: apuntes sobre errores y depuración.
- **`pytest.ini`**: configuración de ejecución.

## Instalación

Se necesita **Python**, `pip` y Microsoft Edge. Desde la raíz del proyecto:

### 1. Crear y activar un entorno virtual (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 3. Preparar Microsoft Edge para Playwright

```powershell
python -m playwright install msedge
```

## Ejecutar los tests

Todos los tests:

```powershell
python -m pytest -v
```

Un módulo concreto:

```powershell
python -m pytest tests_basic/test_tables.py -v
```

Un test por nombre:

```powershell
python -m pytest -k test_clear_context_cookies -v
```

Mostrar la salida de `print()`:

```powershell
python -m pytest -v -s
```

El archivo `pytest.ini` configura la ejecución **con Microsoft Edge visible** (`--browser-channel=msedge` y `--headed`) y la URL base `https://www.playwrightautomation.com/`. Por ello, la fixture puede navegar con `page.goto("/practice.html")`.

## Cómo se organizan las pruebas

El proyecto aplica **Page Object Model**: los archivos de `pages/` encapsulan la interacción con la interfaz y los archivos de `tests_basic/` verifican el resultado esperado.

La fixture `practice_page` utiliza la fixture `page` de `pytest-playwright`, navega a la web de prácticas y entrega la página al test. Algunos tests de contextos utilizan directamente la fixture `browser` para crear contextos independientes.

## Cookies y Storage State

Los tests de Browser Context incluyen ejemplos de:

- Crear contextos aislados.
- Añadir, consultar y eliminar cookies.
- Guardar cookies y datos de `localStorage` con `context.storage_state(path="storage_state.json")`.
- Crear otro contexto con `browser.new_context(storage_state="storage_state.json")`.

**Nota:** algunos tests de carga de estado necesitan que exista previamente `storage_state.json`, generado por el test de guardado. Esto es una dependencia propia de los ejercicios actuales y puede mejorarse en el futuro mediante fixtures que preparen el estado de forma independiente.

**Seguridad:** un archivo de Storage State puede contener datos de autenticación. No debe subirse al repositorio si contiene sesiones reales. Conviene incluir `storage_state.json` y `playwright/.auth/` en `.gitignore`. Si ya se han añadido a Git, ignorarlos no los elimina automáticamente del seguimiento.