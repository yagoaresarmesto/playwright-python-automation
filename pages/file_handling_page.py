from pathlib import Path
from playwright.sync_api import Page

# Locators y acciones del módulo 3: File Handling.
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

        self.multiple_reset = page.get_by_test_id(
            "btn-reset-multiple"
        )

        self.multiple_upload = page.get_by_label(
            "Upload Multiple Files",
        )

        self.multiple_count = page.get_by_test_id(
            "upload-multiple-count"
        )

        self.multiple_result = page.get_by_test_id(
            "upload-multiple-result"
        )

        self.multiple_status = page.get_by_test_id(
            "upload-multiple-status"
        )

    def upload_single_file(self, file_path: Path):
        self.single_upload.set_input_files(file_path)

    def upload_multiple_files(self, file_paths: list[Path]):
        self.multiple_upload.set_input_files(file_paths)

    def reset_single_file(self):
        self.single_reset.click()

    def reset_multiple_files(self):
        self.multiple_reset.click()