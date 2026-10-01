from playwright.sync_api import Page, expect
from pathlib import Path


def test_basic_form_interactions(practice_page: Page):
        page = practice_page

        # TEXT INPUTS

        # Existen distintas formas de localizar un elemento:
        #
        # page.get_by_label("Name", exact=True)
        # page.get_by_placeholder("Enter your name")
        # page.get_by_test_id("input-name")z
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

def test_single_file_upload(practice_page: Page):
    page = practice_page

    upload_input = page.get_by_label("Upload Single File")
    file_path = Path("test_data/sample_upload.txt")

    upload_input.set_input_files(file_path)

    selected_file = page.get_by_test_id("upload-single-result")
    upload_status = page.get_by_test_id("upload-single-status")

    expect(selected_file).to_have_text("sample_upload.txt")
    expect(upload_status).to_be_visible()
    expect(upload_status).to_have_text("✓ File Uploaded Successfully")

def test_multiple_files_upload(practice_page: Page):
    page = practice_page

    upload_input = page.get_by_label("Upload Multiple Files")
    file_path = Path("test_data/sample_upload.txt")
    file_path2 = Path("test_data/sample_upload2.txt")

    upload_input.set_input_files([file_path, file_path2])

    count_files= page.get_by_test_id("upload-multiple-count")
    selected_files = page.get_by_test_id("upload-multiple-result")
    upload_status = page.get_by_test_id("upload-multiple-status")


    expect(count_files).to_have_text("2")
    expect(selected_files).to_have_text("sample_upload.txt, sample_upload2.txt")
    expect(upload_status).to_be_visible()
    expect(upload_status).to_have_text("✓ 2 Files Uploaded Successfully")