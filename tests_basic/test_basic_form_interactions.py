from playwright.sync_api import Page, expect
from pathlib import Path

from pages.file_handling_page import FileHandlingPage
from pages.form_controls_page import FormControlsPage
from pages.javascript_alerts_page import JavaScriptAlertsPage


# MODULE 1 — Form Controls | Text Inputs, Radio Buttons, Checkboxes y Dropdown
# Verifica las interacciones básicas y el envío correcto del formulario.
def test_basic_form_interactions(practice_page: Page):
        page = practice_page

        # TEXT INPUTS

        # Existen distintas formas de localizar un elemento:
        #
        # page.get_by_label("Name", exact=True)
        # page.get_by_placeholder("Enter your name")
        # page.get_by_test_id("input-name")
        # page.locator("#name")
        # page.locator('input[name="name"]')
        #
        # En este caso usamos get_by_label() porque el campo tiene
        # un label asociado y expresa claramente cómo lo identifica el usuario.

        name_input = page.get_by_label("Name", exact=True)
        email_input = page.get_by_label("Email", exact=True)
        address_input = page.get_by_label("Address", exact=True)

        # fill() introduce o reemplaza el contenido del campo.
        name_input.fill("Yago")
        email_input.fill("yagofingoi1234@gmail.com")
        address_input.fill("Bispo Aguirre")

        # Comprobamos que los campos contienen los valores esperados.
        expect(name_input).to_have_value("Yago")
        expect(email_input).to_have_value("yagofingoi1234@gmail.com")
        expect(address_input).to_have_value("Bispo Aguirre")

        # Ejemplo para provocar intencionadamente un AssertionError:
        # expect(name_input).to_have_value("Pedro")

        # RADIO BUTTON

        gender_male = page.get_by_label("Male", exact=True)
        gender_female = page.get_by_label("Female", exact=True)

        # check() selecciona el radio button.
        gender_male.check()

        # Comprobamos que Male está seleccionado y Female no lo está.
        expect(gender_male).to_be_checked()
        expect(gender_female).not_to_be_checked()

        # CHECKBOX

        checkbox_sunday = page.get_by_label("Sunday", exact=True)

        # Marcamos el checkbox y verificamos su estado.
        checkbox_sunday.check()
        expect(checkbox_sunday).to_be_checked()

        # Lo desmarcamos y comprobamos que ya no está seleccionado.
        checkbox_sunday.uncheck()
        expect(checkbox_sunday).not_to_be_checked()

        # DROPDOWN / SELECT

        country_dropdown = page.get_by_label("Select Country", exact=True)

        # Seleccionamos una opción utilizando el atributo value del <option>.
        country_dropdown.select_option("united-kingdom")

        # Comprobamos que el value seleccionado es el esperado.
        expect(country_dropdown).to_have_value("united-kingdom")

        # También podríamos seleccionar por el texto visible:
        # country_dropdown.select_option(label="United Kingdom")

        # SUBMIT BUTTON

        # Utilizamos data-testid porque en la página existen varios botones
        # con el texto "Submit" y queremos identificar este de forma inequívoca.
        submit_button = page.get_by_test_id("btn-submit-text-inputs")
        submit_button.click()

        # RESULTADO DEL FORMULARIO

        status = page.get_by_test_id("text-inputs-status")

        # Comprueba el texto que contiene el elemento:
        expect(status).to_have_text("submitted")

        # Comprueba valores almacenados en atributos HTML del elemento.
        expect(status).to_have_attribute("data-status", "submitted")
        expect(status).to_have_attribute("data-invalid-count", "0")


# MODULE 1 — Form Controls | Text Inputs
# Verifica los mensajes de validación al enviar los campos obligatorios vacíos.

def test_required_fields_validation(practice_page: Page):
    page = practice_page

    submit_button = page.get_by_test_id("btn-submit-text-inputs")
    submit_button.click()

    name_error = page.get_by_test_id("error-name")
    email_error = page.get_by_test_id("error-email")
    address_error = page.get_by_test_id("error-address")

    expect(name_error).to_be_visible()
    expect(name_error).to_have_text("Name is required.")

    expect(email_error).to_be_visible()
    expect(email_error).to_have_text("Email is required.")

    expect(address_error).to_be_visible()
    expect(address_error).to_have_text("Address is required.")


# MODULE 1 — Form Controls | Toggle Switches — Enable Notifications
# Comprueba el estado inicial desmarcado y que el interruptor puede activarse y desactivarse.
def test_toggle_notifications(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # El interruptor debe aparecer desmarcado al cargar la página.
    expect(form_page.toggle_notifications).not_to_be_checked()

    # Activarlo y verificar que queda marcado.
    form_page.enable_notifications()
    expect(form_page.toggle_notifications).to_be_checked()

    # Desactivarlo y comprobar que vuelve al estado inicial.
    form_page.disable_notifications()
    expect(form_page.toggle_notifications).not_to_be_checked()


# MODULE 1 — Form Controls | Toggle Switches — Email Alerts y Auto Save
# Comprueba que los dos interruptores cambian de estado de forma independiente.
def test_toggle_email_alerts_and_autosave(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Estado inicial: Email Alerts marcado y Auto Save desmarcado.
    # No modificamos los controles antes de comprobar sus valores por defecto.
    expect(form_page.toggle_email_alerts).to_be_checked()
    expect(form_page.toggle_autosave).not_to_be_checked()

    # Desactivar Email Alerts sin alterar el estado de Auto Save.
    form_page.disable_email_alerts()
    expect(form_page.toggle_email_alerts).not_to_be_checked()
    expect(form_page.toggle_autosave).not_to_be_checked()

    # Activar Auto Save y comprobar que Email Alerts continúa desmarcado.
    form_page.enable_autosave()
    expect(form_page.toggle_email_alerts).not_to_be_checked()
    expect(form_page.toggle_autosave).to_be_checked()

    # Reactivar Email Alerts y verificar que ambos quedan marcados.
    form_page.enable_email_alerts()
    expect(form_page.toggle_email_alerts).to_be_checked()
    expect(form_page.toggle_autosave).to_be_checked()


# MODULE 1 — Form Controls | Show / Hide Elements
# Verifica que el campo se oculta con Hide y vuelve a mostrarse con Show.
def test_show_hide_element(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    expect(form_page.showhide_textbox).to_be_visible()

    form_page.hide_element()

    expect(form_page.showhide_textbox).to_be_hidden()

    form_page.show_element()

    expect(form_page.showhide_textbox).to_be_visible()


# MODULE 1 — Form Controls | Show / Hide Elements — Hide dos veces
# Verifica que la primera pulsación cambia el estado y la segunda no produce cambios.
def test_hide_element_twice(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    expect(form_page.showhide_textbox).to_be_visible()

    form_page.hide_element()

    expect(form_page.showhide_status).to_have_attribute("data-outcome", "changed")

    expect(form_page.showhide_textbox).to_be_hidden()

    form_page.hide_element()

    expect(form_page.showhide_status).to_have_attribute("data-outcome", "no-change")

    expect(form_page.showhide_textbox).to_be_hidden()

# MODULE 1 — Form Controls | Show / Hide Elements — Show dos veces
# Tras ocultar el campo, verifica que el primer Show lo muestra y el segundo no cambia su estado.
def test_show_element_twice(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    expect(form_page.showhide_textbox).to_be_visible()

    form_page.hide_element()

    expect(form_page.showhide_status).to_have_attribute("data-outcome", "changed")

    expect(form_page.showhide_textbox).to_be_hidden()

    form_page.show_element()

    expect(form_page.showhide_status).to_have_attribute("data-outcome", "changed")

    expect(form_page.showhide_textbox).to_be_visible()

    form_page.show_element()

    expect(form_page.showhide_status).to_have_attribute("data-outcome", "no-change")

    expect(form_page.showhide_textbox).to_be_visible()


# MODULE 1 — Form Controls | Hidden Elements & AJAX — Toggle Input Box 2
# Comprueba el estado inicial y que cada pulsación alterna la visibilidad y el mensaje de estado.
def test_toggle_input_box_2(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    expect(form_page.ajax_input_2).to_be_hidden()

    expect(form_page.ajax_status).to_have_text(
        "Ready"
    )

    form_page.toggle_input_2()

    expect(form_page.ajax_input_2).to_be_visible()

    expect(form_page.ajax_status).to_have_text(
        "Input Box 2 shown"
    )

    form_page.toggle_input_2()

    expect(form_page.ajax_input_2).to_be_hidden()

    expect(form_page.ajax_status).to_have_text(
        "Input Box 2 hidden"
    )


# MODULE 1 — Form Controls | Hidden Elements & AJAX — Load AJAX Content
# Comprueba el contenido inicial y espera el título insertado tras la carga asíncrona.
def test_load_ajax_content(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    expect(form_page.ajax_status).to_have_text(
        "Ready"
    )

    expect(form_page.ajax_content).to_have_text(
        "No content loaded yet."
    )

    form_page.load_ajax_content()

    expect(form_page.ajax_status).to_have_text(
        "AJAX content loaded"
    )

    # Verificamos solo el título: el contenedor también incluye un párrafo.
    # expect() reintenta la comprobación mientras aparece el contenido AJAX.
    expect(form_page.ajax_loaded_heading).to_have_text(
        "AJAX Content Loaded"
    )

# Alternativa menos específica: comprobar que el contenedor incluye el texto.
# expect(form_page.ajax_content).to_contain_text("AJAX Content Loaded")

# MODULE 3 — File Handling | Single File Upload
# Verifica la selección de un archivo y el mensaje de éxito.
def test_single_file_upload(practice_page: Page):
    file_handling = FileHandlingPage(practice_page)

    file_path = Path("test_data/sample_upload.txt")


    file_handling.upload_single_file(file_path)

    expect(file_handling.single_result).to_have_text(
        "sample_upload.txt"
    )

    expect(file_handling.single_status).to_be_visible()
    expect(file_handling.single_status).to_have_text(
        "✓ File Uploaded Successfully"
    )

# MODULE 3 — File Handling | Multiple File Upload
# Verifica la cantidad, los nombres y el estado de dos archivos seleccionados.
def test_multiple_files_upload(practice_page: Page):
    # 1. Crear el Page Object.
    file_handling = FileHandlingPage(practice_page)

    # 2. Preparar los archivos.
    file_path = Path("test_data/sample_upload.txt")
    file_path2 = Path("test_data/sample_upload2.txt")

    # 3. Subir ambos archivos.
    file_handling.upload_multiple_files([file_path, file_path2])

    # 4. Comprobar los resultados.
    expect(file_handling.multiple_count).to_have_text("2")

    expect(file_handling.multiple_result).to_have_text(
        "sample_upload.txt, sample_upload2.txt"
    )

    expect(file_handling.multiple_status).to_be_visible()

    expect(file_handling.multiple_status).to_have_text(
        "✓ 2 Files Uploaded Successfully"
    )


# MODULE 3 — File Handling | Single File Upload — Reset
# Verifica que Reset limpia el archivo seleccionado, el mensaje y el input.
def test_single_file_upload_reset(practice_page: Page):
    file_handling = FileHandlingPage(practice_page)

    file_path = Path("test_data/sample_upload.txt")

    # 1. Subir el archivo.
    file_handling.upload_single_file(file_path)

    # 2. Verificar que se seleccionó correctamente.
    expect(file_handling.single_result).to_have_text("sample_upload.txt")

    # 3. Restablecer el formulario.
    file_handling.reset_single_file()

    # 4. Verificar que se ha limpiado.
    expect(file_handling.single_result).to_have_text("—")
    expect(file_handling.single_status).to_be_empty()
    expect(file_handling.single_upload).to_have_value("")


# MODULE 3 — File Handling | Multiple File Upload — Reset
# Verifica que Reset limpia los nombres, el estado, el contador y el input múltiple.
def test_multiple_files_upload_reset(practice_page: Page):
    file_handling = FileHandlingPage(practice_page)

    file_path = Path("test_data/sample_upload.txt")
    file_path2 = Path("test_data/sample_upload2.txt")

    # Seleccionar dos archivos.
    file_handling.upload_multiple_files([file_path, file_path2])
    expect(file_handling.multiple_count).to_have_text("2")

    # Restablecer la selección.
    file_handling.reset_multiple_files()

    # Comprobar que todo vuelve al estado inicial.
    expect(file_handling.multiple_result).to_have_text("—")
    expect(file_handling.multiple_status).to_be_empty()
    expect(file_handling.multiple_count).to_have_text("0")
    expect(file_handling.multiple_upload).to_have_value("")


# MODULE 5 — JavaScript Alerts | Simple Alert
# Verifica el mensaje de una alerta nativa, la acepta y comprueba
# que la página muestra la confirmación correspondiente.

def test_simple_alert(practice_page: Page):
    # Creamos el Page Object para acceder a los elementos y acciones.
    alerts_page = JavaScriptAlertsPage(practice_page)

    # Esta función se ejecutará automáticamente cuando aparezca
    # el diálogo JavaScript.
    def handle_dialog(dialog):
        # Comprobamos que el diálogo es de tipo alert.
        assert dialog.type == "alert"

        # Verificamos el mensaje exacto mostrado por el navegador.
        assert dialog.message == "I am an alert box!"

        # Aceptamos la alerta (equivale a pulsar "Aceptar").
        dialog.accept()

    # Registramos el manejador ANTES de abrir la alerta.
    # once() escucha únicamente el siguiente evento "dialog".
    practice_page.once("dialog", handle_dialog)

    # Pulsamos el botón que provoca la aparición de la alerta.
    # Playwright ejecutará handle_dialog cuando esta aparezca.
    alerts_page.open_simple_alert()

    # Después de aceptar la alerta, comprobamos que la aplicación
    # muestra el mensaje de confirmación esperado en el DOM.
    expect(alerts_page.alert_result).to_have_text(
        "Alert accepted."
    )

# MODULE 5 — JavaScript Alerts | Confirmation Alert — Aceptar
# Comprueba el mensaje del diálogo y la respuesta de la página al aceptarlo.
def test_confirm_alert_accept(practice_page: Page):
    alerts_page = JavaScriptAlertsPage(practice_page)

    def handle_dialog(dialog):
        # Comprobamos que es un diálogo de confirmación.
        assert dialog.type == "confirm"

        # Verificamos el mensaje mostrado por el navegador.
        assert dialog.message == "Press a button!"

        # Aceptamos la confirmación (equivale a pulsar "Aceptar").
        dialog.accept()

    # Escuchamos el siguiente diálogo antes de abrirlo.
    practice_page.once("dialog", handle_dialog)

    # Abrimos la confirmación y verificamos su resultado tras aceptarla.
    alerts_page.open_confirm_alert()

    # Comprobamos que la página registra que hemos aceptado.
    expect(alerts_page.confirm_result).to_have_text(
        "You pressed OK!"
    )


# MODULE 5 — JavaScript Alerts | Confirmation Alert — Cancelar
# Verifica que cancelar el diálogo muestra el resultado esperado.

def test_confirm_alert_dismiss(practice_page: Page):
    alerts_page = JavaScriptAlertsPage(practice_page)

    def handle_dialog(dialog):
        # Comprobamos que es un diálogo de confirmación.
        assert dialog.type == "confirm"

        # Verificamos el mensaje mostrado por el navegador.
        assert dialog.message == "Press a button!"

        # Cancelamos la confirmación (equivale a pulsar "Cancelar").
        dialog.dismiss()

    # Registramos el manejador antes de abrir el diálogo.
    practice_page.once("dialog", handle_dialog)

    # Abrimos el diálogo de confirmación.
    alerts_page.open_confirm_alert()

    # Comprobamos que la página registra que hemos cancelado.
    expect(alerts_page.confirm_result).to_have_text(
        "You pressed Cancel!"
    )

# MODULE 5 — JavaScript Alerts | Prompt Alert — Introducir nombre y aceptar
# Envía un nombre al diálogo y comprueba que aparece en el saludo.
def test_prompt_alert_accept(practice_page: Page):
    alerts_page = JavaScriptAlertsPage(practice_page)

    def handle_dialog(dialog):
        # Comprobamos que es un diálogo de prompt.
        assert dialog.type == "prompt"

        # Verificamos el mensaje mostrado por el navegador.
        assert dialog.message == "Please enter your name:"

        # Introducimos el nombre "Yago" y aceptamos el prompt.
        dialog.accept("Yago")

    # Registramos el manejador antes de abrir el prompt.
    practice_page.once("dialog", handle_dialog)

    # Abrimos el prompt; el manejador lo acepta o cancela.
    alerts_page.open_prompt_alert()

    # Verificamos la respuesta que muestra la aplicación en el DOM.
    expect(alerts_page.prompt_result).to_have_text(
        "Hello Yago! How are you today?"
    )

# MODULE 5 — JavaScript Alerts | Prompt Alert — Cancelar
# Verifica que cancelar el diálogo no envía un nombre y muestra el aviso esperado.
def test_prompt_alert_dismiss(practice_page: Page):
    alerts_page = JavaScriptAlertsPage(practice_page)

    def handle_dialog(dialog):
        # Comprobamos que es un diálogo de prompt.
        assert dialog.type == "prompt"

        # Verificamos el mensaje mostrado por el navegador.
        assert dialog.message == "Please enter your name:"

        # Cancelamos el prompt sin enviar ningún nombre.
        dialog.dismiss()

    # Registramos el manejador antes de abrir el prompt.
    practice_page.once("dialog", handle_dialog)

    # Abrimos el prompt; el manejador lo acepta o cancela.
    alerts_page.open_prompt_alert()

    # Verificamos la respuesta que muestra la aplicación en el DOM.
    expect(alerts_page.prompt_result).to_have_text(
        "User cancelled the prompt."
    )

# MODULE 5 — JavaScript Alerts | Prompt Alert — Aceptar texto vacío
# Comprueba el valor inicial y cómo responde la página al enviar una cadena vacía.
def test_prompt_alert_empty(practice_page: Page):
    alerts_page = JavaScriptAlertsPage(practice_page)

    def handle_dialog(dialog):
        # Comprobamos que es un diálogo de prompt.
        assert dialog.type == "prompt"

        # Verificamos el mensaje mostrado por el navegador.
        assert dialog.message == "Please enter your name:"

        # Comprobamos que el prompt muestra "Rajesh" como valor inicial.
        assert dialog.default_value == "Rajesh"

        # Aceptamos el prompt enviando una cadena vacía.
        # El valor enviado es "", aunque la aplicación muestre luego "Rajesh".
        dialog.accept("")

    # Registramos el manejador antes de abrir el prompt.
    practice_page.once("dialog", handle_dialog)

    # Abrimos el prompt; el manejador lo acepta o cancela.
    alerts_page.open_prompt_alert()

    # Verificamos la respuesta que muestra la aplicación en el DOM.
    expect(alerts_page.prompt_result).to_have_text(
        "Hello Rajesh! How are you today?"
    )