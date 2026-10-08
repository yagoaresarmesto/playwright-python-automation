from playwright.async_api import Page

class FileHandlingPage:
    def __init__(self, page: Page):
        self.page = page

        self.single_upload = page.get_by_label(
            "Upload Single File",
            exact=True
        )

        self.single_result = page.get_by_test_id(
            "upload-single-result"
        )

        self.single_status = page.get_by_test_id(
            "upload-single-status"
        )

        self.single_reset = page.get_by_test_id(
            "btn-reset-single"
        )