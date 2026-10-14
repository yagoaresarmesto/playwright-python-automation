from playwright.sync_api import Page


class FormControlsPage:
    def __init__(self, page: Page):
        self.page = page

        # Show / Hide Elements: botones, campo cuya visibilidad cambia
        # y registro que indica si la acción produjo un cambio.
        self.hide_button = page.get_by_test_id(
            "btn-hide-element"
        )

        self.show_button = page.get_by_test_id(
            "btn-show-element"
        )

        self.showhide_textbox = page.get_by_test_id(
            "showhide-textbox"
        )

        self.showhide_status = page.get_by_test_id(
            "showhide-log"
        )

        # Hidden Elements & AJAX: controles para alternar la visibilidad
        # del segundo input y consultar el estado de las acciones.
        self.toggle_input_2_button = page.get_by_test_id(
            "btn-toggle-input-2"
        )

        self.ajax_input_2 = page.get_by_test_id(
            "ajax-input-2"
        )

        # Este estado se reutiliza tanto para el toggle como para la carga AJAX.
        self.ajax_status = page.get_by_test_id(
            "ajax-status"
        )

        # AJAX: botón de carga, contenedor del resultado y título insertado
        # después de la operación asíncrona.
        self.load_ajax_button = page.get_by_test_id(
            "btn-load-ajax"
        )

        self.ajax_content = page.get_by_test_id(
            "ajax-content"
        )

        # Localizar el título permite comprobar su texto exacto sin incluir
        # el párrafo que también aparece dentro de ajax_content.
        self.ajax_loaded_heading = page.get_by_test_id(
            "ajax-loaded-heading"
        )

    # Show / Hide Elements: acciones sobre la visibilidad del campo.
    def hide_element(self):
        self.hide_button.click()

    def show_element(self):
        self.show_button.click()

    # Hidden Elements & AJAX: acciones; las assertions van en los tests.
    def toggle_input_2(self):
        self.toggle_input_2_button.click()

    def load_ajax_content(self):
        self.load_ajax_button.click()
