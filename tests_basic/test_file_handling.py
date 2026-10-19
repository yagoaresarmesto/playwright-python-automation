from pathlib import Path
from playwright.sync_api import Page, expect
from pages.file_handling_page import FileHandlingPage

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


