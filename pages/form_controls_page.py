from playwright.sync_api import Page


class FormControlsPage:
    def __init__(self, page: Page):
        self.page = page

        # Show / Hide Elements
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

        # Hidden Elements & AJAX

        self.toggle_input_2_button = page.get_by_test_id(
            "btn-toggle-input-2"
        )
        self.ajax_input_2 = page.get_by_test_id(
            "ajax-input-2"
        )

        self.ajax_status = page.get_by_test_id(
            "ajax-status"
        )


    # Show / Hide Elements methods
    def hide_element(self):
        self.hide_button.click()

    def show_element(self):
        self.show_button.click()

    # Hidden Elements & AJAX methods
    def toggle_input_2(self):
        self.toggle_input_2_button.click()
