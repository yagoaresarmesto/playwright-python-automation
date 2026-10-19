import pytest
from playwright.sync_api import Page, expect
from pages.form_controls_page import FormControlsPage
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


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


# MODULE 1 — Form Controls | Multi Selects — Selección de varias opciones
# Comprueba que un <select multiple> admite varias marcas simultáneamente.
def test_multiselect_clothing_brands(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Seleccionamos tres opciones mediante sus atributos HTML value.
    form_page.select_clothing_brands(["nike", "adidas", "puma"])

    # to_have_values() comprueba todos los valores seleccionados.
    expect(form_page.multiselect_colors).to_have_values(
        ["nike", "adidas", "puma"]
    )


# MODULE 1 — Form Controls | Multi Selects — Textos visibles duplicados
# Puma y Zara aparecen dos veces: sus value permiten distinguir cada opción.
def test_multiselect_duplicate_labels(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Seleccionamos cuatro opciones: dos Puma y dos Zara.
    # Usamos los value y respetamos el orden en el que aparecen en el HTML.
    form_page.select_clothing_brands(["puma", "zara", "puma-alt", "zara-alt"])

    # Verificamos las cuatro opciones, aunque solo haya dos marcas distintas.
    expect(form_page.multiselect_colors).to_have_values(
        ["puma", "zara", "puma-alt", "zara-alt"]
    )


# MODULE 1 — Form Controls | Multi Selects — Sustituir la selección
# Una segunda llamada a select_option() reemplaza los valores seleccionados.
def test_multiselect_replace_selection(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Seleccionamos inicialmente Nike y Adidas.
    form_page.select_clothing_brands(["nike", "adidas"])

    # Verificamos la selección inicial.
    expect(form_page.multiselect_colors).to_have_values(
        ["nike", "adidas"]
    )

    # Sustituimos la selección anterior por Puma y Zara.
    form_page.select_clothing_brands(["puma", "zara"])

    # Solo Puma y Zara deben quedar seleccionadas; Nike y Adidas ya no lo están.
    expect(form_page.multiselect_colors).to_have_values(
        ["puma", "zara"]
    )


# MODULE 1 — Form Controls | Multi Selects — Limpiar la selección
# Pasar una lista vacía a select_option() deselecciona todas las opciones.
def test_multiselect_clear_selection(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Seleccionamos inicialmente Nike y Adidas.
    form_page.select_clothing_brands(["nike", "adidas"])

    # Comprobamos que ambas opciones están seleccionadas.
    expect(form_page.multiselect_colors).to_have_values(
        ["nike", "adidas"]
    )

    # Enviamos una lista vacía para deseleccionar todas las opciones.
    form_page.select_clothing_brands([])

    # La lista esperada también está vacía: no queda ninguna seleccionada.
    expect(form_page.multiselect_colors).to_have_values([])

# MODULE 1 — Form Controls | Tooltip — Mostrar con hover
# Comprueba que el tooltip aparece al pasar el ratón sobre el botón.
def test_tooltip_on_hover(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Comprobamos que el mensaje del tooltip comienza oculto.
    expect(form_page.tooltip_bubble).to_be_hidden()

    # Verificamos que el indicador muestra el estado inicial "hidden".
    expect(form_page.tooltip_state).to_have_text("hidden")

    # Pasamos el cursor sobre el botón Delivery estimate.
    # La acción hover() debe provocar que aparezca el tooltip.
    form_page.show_tooltip()

    # Comprobamos que el mensaje del tooltip es realmente visible.
    expect(form_page.tooltip_bubble).to_be_visible()

    # Verificamos que el mensaje informativo contiene el texto esperado.
    expect(form_page.tooltip_bubble).to_have_text(
        "Standard delivery takes 3–5 working days."
    )

    # Comprobamos que la aplicación actualiza el indicador a "visible".
    expect(form_page.tooltip_state).to_have_text("visible")


# MODULE 1 — Form Controls | Tooltip — Ocultar con mouseleave
# Comprueba que el tooltip desaparece al retirar el cursor del botón.
def test_tooltip_hide_on_mouse_leave(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Verificamos que el tooltip comienza oculto.
    expect(form_page.tooltip_bubble).to_be_hidden()

    # Pasamos el cursor sobre el botón para mostrar el tooltip.
    form_page.show_tooltip()

    # Comprobamos que el tooltip aparece y el indicador cambia a "visible".
    expect(form_page.tooltip_bubble).to_be_visible()
    expect(form_page.tooltip_state).to_have_text("visible")

    # Movemos el cursor a la esquina superior izquierda de la ventana.
    # Al abandonar el botón, se provoca el evento mouseleave.
    practice_page.mouse.move(0, 0)

    # Verificamos que el tooltip desaparece realmente.
    expect(form_page.tooltip_bubble).to_be_hidden()

    # Comprobamos que el indicador vuelve al estado "hidden".
    expect(form_page.tooltip_state).to_have_text("hidden")


# MODULE 1 — Form Controls | Tooltip — Mostrar con focus
# Comprueba que el tooltip aparece cuando el botón recibe el foco.
def test_tooltip_on_focus(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Comprobamos que el tooltip está oculto inicialmente.
    expect(form_page.tooltip_bubble).to_be_hidden()

    # Colocamos el foco directamente sobre el botón Delivery estimate.
    # focus() no necesita mover el cursor del ratón.
    form_page.focus_tooltip()

    # Verificamos que el botón ha recibido el foco del teclado.
    expect(form_page.tooltip_trigger).to_be_focused()

    # Comprobamos que el tooltip aparece como consecuencia del foco.
    expect(form_page.tooltip_bubble).to_be_visible()

    # Verificamos que el indicador de estado cambia a "visible".
    expect(form_page.tooltip_state).to_have_text("visible")


# MODULE 1 — Form Controls | Tooltip — Ocultar al perder el foco
# Comprueba que el tooltip desaparece al cambiar el foco mediante Tab.
def test_tooltip_hide_on_blur(practice_page: Page):
    form_page = FormControlsPage(practice_page)

    # Comprobamos que el tooltip comienza oculto.
    expect(form_page.tooltip_bubble).to_be_hidden()

    # Colocamos el foco sobre el botón Delivery estimate.
    form_page.focus_tooltip()

    # Verificamos que el botón ha recibido el foco.
    expect(form_page.tooltip_trigger).to_be_focused()

    # Comprobamos que el tooltip aparece y el indicador cambia a "visible".
    expect(form_page.tooltip_bubble).to_be_visible()
    expect(form_page.tooltip_state).to_have_text("visible")

    # Simulamos la pulsación de Tab para avanzar al siguiente elemento
    # interactivo y provocar que el botón Delivery estimate pierda el foco.
    practice_page.keyboard.press("Tab")

    # Verificamos que el botón ya no tiene el foco del teclado.
    expect(form_page.tooltip_trigger).not_to_be_focused()

    # Comprobamos que el mensaje del tooltip vuelve a ocultarse.
    expect(form_page.tooltip_bubble).to_be_hidden()

    # Verificamos que el indicador de estado vuelve a mostrar "hidden".
    expect(form_page.tooltip_state).to_have_text("hidden")

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