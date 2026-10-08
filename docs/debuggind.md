# Apuntes — Errores y debugging en Playwright con Python

## 1. Cómo investigar un test que falla

Cuando pytest muestra `FAILED`, no debemos cambiar código a ciegas.

El procedimiento recomendado es:

1. **Localizar la línea que falló** en nuestro archivo de test.
2. **Leer el mensaje final del error**, no solo las primeras líneas del traceback.
3. **Consultar el Call log** de Playwright para saber qué elemento encontró o qué acción intentó realizar.
4. **Identificar la causa**: locator incorrecto, assertion incorrecta, elemento no disponible, problema de navegación, etc.
5. Corregir el problema y volver a ejecutar el test.

**Importante:** un test que falla no significa necesariamente que la aplicación tenga un bug. También puede haber un error en nuestro código de automatización.

---

## 2. Error real: locator que apunta al elemento equivocado

### El problema

Escribimos:

```python
upload_input = page.get_by_label("Multiple File Upload")
upload_input.set_input_files([file_path, file_path2])
```

Y Playwright devolvió:

```text
Locator.set_input_files: Error:
Node is not an HTMLInputElement
```

En el `Call log` aparecía:

```text
locator resolved to:
<button aria-label="Reset Multiple File Upload">
    Reset
</button>
```

### ¿Qué ocurrió?

Queríamos encontrar un `<input type="file">`, pero Playwright encontró un botón.

El texto que habíamos escrito no era el label real del input.

El HTML correcto era:

```html
<label for="upload-multiple">Upload Multiple Files</label>

<input
    type="file"
    id="upload-multiple"
    data-testid="upload-multiple"
    multiple
>
```

### Solución

```python
upload_input = page.get_by_label(
    "Upload Multiple Files",
    exact=True
)
```

O también:

```python
upload_input = page.get_by_test_id("upload-multiple")
```

### ¿Qué aprendimos?

- `get_by_label()` busca el nombre accesible del control, no necesariamente el título visual de una sección.
- Sin `exact=True`, puede haber coincidencias parciales.
- `exact=True` evita coincidencias parciales, pero no corrige un texto mal escrito.
- El `Call log` permite ver el elemento HTML que Playwright encontró realmente.

---

## 3. Playwright Inspector — debugging en directo

El Inspector sirve para **pausar un test mientras se ejecuta** e investigar la página.

### Cómo abrirlo

Añadir temporalmente:

```python
page.pause()
```

Ejemplo:

```python
def test_multiple_files_upload(practice_page: Page):
    page = practice_page

    upload_input = page.get_by_label(
        "Upload Multiple Files",
        exact=True
    )

    page.pause()

    upload_input.set_input_files([
        Path("test_data/sample_upload.txt"),
        Path("test_data/sample_upload2.txt")
    ])
```

Ejecutar el test con navegador visible:

```bash
pytest tests_basic/test_basic_form_interactions.py::test_multiple_files_upload
```

### Funciones principales

**Pick Locator (selector de elementos)**

Permite señalar un elemento de la página y obtener sugerencias de locators.

Por ejemplo:

```python
page.get_by_text("Multiple File Upload")
```

Pero hay que comprobar qué elemento se seleccionó: podría ser el título de la sección y no el input que queremos utilizar.

**Resume (▶)**

Continúa la ejecución después de `page.pause()`.

**Record**

Graba interacciones y genera código Playwright. Puede ser útil para explorar, pero el código generado debe revisarse.

### Cuándo utilizarlo

Cuando queremos:

- Investigar por qué un locator no encuentra el elemento esperado.
- Examinar el estado de la página durante la ejecución.
- Probar locators antes de incorporarlos al test.
- Seguir paso a paso un comportamiento problemático.

**Recordatorio:** eliminar `page.pause()` cuando terminemos de depurar.

---

## 4. Trace Viewer — debugging después de la ejecución

El Trace Viewer permite investigar una ejecución **una vez que el test ha terminado**.

Es especialmente útil cuando un test falla en CI/CD y no podemos observarlo en directo.

### Generar traces

Guardar traces solo de los tests fallidos:

```bash
pytest --tracing=retain-on-failure
```

Guardar traces de todos los tests:

```bash
pytest --tracing=on
```

Ejecutar un test concreto:

```bash
pytest tests_basic/test_basic_form_interactions.py::test_multiple_files_upload --tracing=retain-on-failure
```

Los archivos se guardan normalmente dentro de:

```text
test-results/
└── carpeta-del-test/
    └── trace.zip
```

### Abrir un trace

```bash
playwright show-trace "ruta/al/trace.zip"
```

En Windows, desde PowerShell, podemos buscarlo con:

```powershell
Get-ChildItem -Path .\test-results -Filter trace.zip -Recurse
```

### Partes principales del Trace Viewer

| Zona | Para qué sirve |
|---|---|
| Timeline superior | Ver la secuencia temporal de la ejecución |
| Actions | Consultar las acciones ejecutadas y sus duraciones |
| Before / After | Examinar el estado de la página antes y después de una acción |
| Call | Revisar los argumentos de una llamada |
| Errors | Consultar errores asociados a la ejecución |
| Log | Examinar mensajes de ejecución |
| Network | Investigar peticiones de red |
| Source | Relacionar acciones con código fuente cuando está disponible |

---

## 5. Error real: assertion incorrecta

En nuestro test de múltiples archivos escribimos intencionadamente:

```python
expect(count_files).to_have_text("3")
```

Pero habíamos subido dos archivos.

La aplicación mostraba:

```html
<span data-testid="upload-multiple-count">2</span>
```

Playwright esperó hasta agotar el timeout de la assertion porque el texto no coincidía.

### Cómo lo investigamos

1. Abrimos `trace.zip`.
2. Buscamos la acción `Set input files`.
3. Comprobamos que el test había asignado los archivos.
4. Seleccionamos la acción `Expect "to have text"`.
5. Vimos que el valor esperado era `"3"`.

La corrección fue:

```python
expect(count_files).to_have_text("2")
```

### ¿Qué aprendimos?

**Distinguir un bug de la aplicación de un error del test.**

El hecho de que una assertion falle no demuestra por sí solo que la web funcione incorrectamente.

También recordamos que `to_have_text()` comprueba texto:

```python
expect(count_files).to_have_text("2")
```

No:

```python
expect(count_files).to_have_text(2)
```

---

## 6. Assertions y esperas automáticas

Las assertions de Playwright como:

```python
expect(locator).to_be_visible()
expect(locator).to_have_text("submitted")
expect(locator).to_have_value("Yago")
```

reintentan la comprobación durante un tiempo limitado.

Esto es útil porque las interfaces web pueden actualizarse de manera asíncrona.

Si el estado esperado no aparece dentro del timeout, el test falla.

**No debemos solucionar estos fallos añadiendo automáticamente:**

```python
page.wait_for_timeout(5000)
```

Primero hay que averiguar si el locator, la condición esperada o el comportamiento de la aplicación son correctos.

---

## 7. Comandos de consulta rápida

| Objetivo | Comando |
|---|---|
| Ejecutar toda la suite | `pytest` |
| Ejecutar un archivo | `pytest tests_basic/test_basic_form_interactions.py` |
| Ejecutar un test | `pytest tests_basic/test_basic_form_interactions.py::test_multiple_files_upload` |
| Ver los `print()` | `pytest -s` |
| Guardar traces al fallar | `pytest --tracing=retain-on-failure` |
| Guardar todos los traces | `pytest --tracing=on` |
| Abrir un trace | `playwright show-trace "ruta/trace.zip"` |

## 8. Guía rápida de decisión

**¿Un locator encuentra el elemento incorrecto?**

→ Revisar el HTML y el `Call log`. Utilizar Inspector para comprobar el locator.

**¿Una assertion falla?**

→ Comparar el valor esperado con el valor real. Revisar el estado de la página y el trace.

**¿Un test falla solo algunas veces?**

→ Investigar sincronización, cambios de estado, dependencias entre tests y peticiones de red. No añadir esperas fijas sin diagnóstico.

**¿Un test falla en GitHub Actions o en otro entorno?**

→ Consultar los logs y el trace generado durante esa ejecución.

**¿El test se queda esperando demasiado?**

→ Examinar qué acción está bloqueada y qué condición necesita Playwright para continuar.

---

## Idea principal

**Inspector = investigar mientras el test se ejecuta.**

**Trace Viewer = investigar después de que el test se ejecutó.**

**Traceback + Call log = primer lugar donde mirar cuando pytest muestra `FAILED`.**

La habilidad importante no es memorizar todos los errores, sino aprender a localizar la causa antes de modificar el código.