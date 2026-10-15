
from playwright.sync_api import Page


class FormControlsPage:
    """
    Page Object de los controles interactivos de la página Practice.

    Centraliza los locators y las acciones sobre los elementos.
    Las comprobaciones (assertions) se realizan en los tests.
    """

    def __init__(self, page: Page):
        # Guardamos la página para poder reutilizarla si fuera necesario.
        self.page = page

        # SHOW / HIDE ELEMENTS — LOCATORS
        # Botones para mostrar u ocultar un campo de texto.
        self.hide_button = page.get_by_test_id(
            "btn-hide-element"
        )

        self.show_button = page.get_by_test_id(
            "btn-show-element"
        )

        # Campo cuya visibilidad cambia al pulsar Hide o Show.
        self.showhide_textbox = page.get_by_test_id(
            "showhide-textbox"
        )

        # Registro del resultado de la acción.
        # El atributo data-outcome permite distinguir entre:
        # - "changed": la acción modificó el estado.
        # - "no-change": el elemento ya estaba en ese estado.
        self.showhide_status = page.get_by_test_id(
            "showhide-log"
        )

        # TOGGLE SWITCHES — LOCATORS
        # Aunque visualmente son interruptores, en HTML son checkboxes.
        # Por eso podemos utilizar check(), uncheck() y to_be_checked().
        #
        # Notifications comienza desmarcado.
        self.toggle_notifications = page.get_by_test_id(
            "toggle-notifications"
        )

        # Email Alerts comienza marcado por defecto.
        self.toggle_email_alerts = page.get_by_test_id(
            "toggle-email-alerts"
        )

        # Auto Save comienza desmarcado.
        self.toggle_autosave = page.get_by_test_id(
            "toggle-autosave"
        )

        # HIDDEN ELEMENTS & AJAX — LOCATORS
        # Botón que alterna la visibilidad de Input Box 2.
        self.toggle_input_2_button = page.get_by_test_id(
            "btn-toggle-input-2"
        )

        # Campo que aparece o desaparece al pulsar el botón anterior.
        self.ajax_input_2 = page.get_by_test_id(
            "ajax-input-2"
        )

        # Mensaje de estado compartido por las acciones de esta sección.
        # Por ejemplo: "Ready", "Input Box 2 shown" o
        # "AJAX content loaded".
        self.ajax_status = page.get_by_test_id(
            "ajax-status"
        )

        # Botón que inicia la carga asíncrona de contenido.
        self.load_ajax_button = page.get_by_test_id(
            "btn-load-ajax"
        )

        # Contenedor donde aparece el contenido cargado mediante AJAX.
        # Puede incluir varios elementos, como un título y un párrafo.
        self.ajax_content = page.get_by_test_id(
            "ajax-content"
        )

        # Título insertado tras la carga AJAX.
        # Utilizar un locator específico permite comprobar su texto
        # exacto con to_have_text(), sin incluir el resto del contenedor.
        self.ajax_loaded_heading = page.get_by_test_id(
            "ajax-loaded-heading"
        )

    # SHOW / HIDE ELEMENTS — ACCIONES
    # click() reproduce la pulsación del usuario sobre un botón.

    def hide_element(self):
        # Solicita ocultar el campo.
        self.hide_button.click()

    def show_element(self):
        # Solicita mostrar el campo.
        self.show_button.click()

    # TOGGLE SWITCHES — ACCIONES
    # check() garantiza que el checkbox termine marcado.
    # uncheck() garantiza que termine desmarcado.
    #
    # A diferencia de click(), estas operaciones no invierten
    # innecesariamente un estado que ya es el deseado.
    #
    # Las comprobaciones del estado inicial y final corresponden
    # a los tests mediante to_be_checked() y not_to_be_checked().

    def enable_notifications(self):
        # Activa el interruptor de notificaciones.
        self.toggle_notifications.check()

    def disable_notifications(self):
        # Desactiva el interruptor de notificaciones.
        self.toggle_notifications.uncheck()

    def enable_email_alerts(self):
        # Activa las alertas por correo electrónico.
        self.toggle_email_alerts.check()

    def disable_email_alerts(self):
        # Desactiva las alertas por correo electrónico.
        self.toggle_email_alerts.uncheck()

    def enable_autosave(self):
        # Activa el guardado automático.
        self.toggle_autosave.check()

    def disable_autosave(self):
        # Desactiva el guardado automático.
        self.toggle_autosave.uncheck()

    # HIDDEN ELEMENTS & AJAX — ACCIONES

    def toggle_input_2(self):
        # Alterna la visibilidad de Input Box 2.
        # El test verifica el nuevo estado y el mensaje correspondiente.
        self.toggle_input_2_button.click()

    def load_ajax_content(self):
        # Inicia la carga AJAX.
        # El test espera y verifica el contenido mediante expect(),
        # sin necesidad de utilizar time.sleep().
        self.load_ajax_button.click()

