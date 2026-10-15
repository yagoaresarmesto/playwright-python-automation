from playwright.sync_api import Page


class JavaScriptAlertsPage:
    def __init__(self, page: Page):
        self.page = page

        # MODULE 5 — JavaScript Alerts
        # Botón que abre una alerta nativa del navegador.
        self.simple_alert_button = page.get_by_test_id(
            "btn-simple-alert"
        )

        # Botón que abre un diálogo de confirmación.
        self.confirm_alert_button = page.get_by_test_id(
            "btn-confirm-alert"
        )

        # Botón que abre un diálogo para introducir texto.
        self.prompt_alert_button = page.get_by_test_id(
            "btn-prompt-alert"
        )

        # Resultado mostrado en la página después de gestionar la alerta.
        self.alert_result = page.get_by_test_id(
            "alert-result"
        )

        self.confirm_result = page.get_by_test_id(
            "confirm-result"
        )

        # Resultado mostrado por la página tras aceptar o cancelar el prompt.
        self.prompt_result = page.get_by_test_id(
            "prompt-result"
        )

    def open_simple_alert(self):
        # Ejecuta la acción que provoca la aparición del diálogo.
        self.simple_alert_button.click()

    def open_confirm_alert(self):
        # Abre el diálogo de confirmación del navegador.
        self.confirm_alert_button.click()

    def open_prompt_alert(self):
        # Abre el diálogo JavaScript que solicita un nombre.
        self.prompt_alert_button.click()