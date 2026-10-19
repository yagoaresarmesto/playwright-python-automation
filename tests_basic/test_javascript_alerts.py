from playwright.sync_api import Page, expect
from pages.javascript_alerts_page import JavaScriptAlertsPage

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