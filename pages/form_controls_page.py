from playwright.sync_api import Page


class FormControlsPage:
    def __init__(self, page: Page):
        self.page = page

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

    def hide_element(self):
        self.hide_button.click()

    def show_element(self):
        self.show_button.click()



