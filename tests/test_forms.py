import pytest
from app import create_app
from wtforms import SubmitField, SelectField, TextAreaField
from app.forms import RegistrationForm, LoginForm, AssetForm, CustomerForm, ManufacturerForm

# The following code disables CSRF protection to enable the Pytest unit tests that follow to run, which check the validation (or expected data) for each of the forms in the application (the registration form, login form, asset form, customer form, and manufacturer form)


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


def test_registration_form(app):
    with app.app_context():
        form = RegistrationForm(
            username="testuser", password="testpassword", confirm_password="testpassword")
        assert form.validate() == True


def test_blank_registration_form(app):
    with app.app_context():
        form = RegistrationForm()
        assert form.validate() == False


def test_incorrect_registration_form(app):
    with app.app_context():
        form = RegistrationForm(
            username="testuser", password="password", confirm_password="testuser")
        assert form.validate() == False


def test_login_form(app):
    with app.app_context():
        form = LoginForm(username="testuser", password="testpassword")
        assert form.validate() == True


def test_asset_form(app):
    with app.app_context():
        form = AssetForm()

        assert isinstance(form.category, SelectField)
        assert isinstance(form.comments, TextAreaField)
        assert isinstance(form.customer, SelectField)
        assert isinstance(form.manufacturer, SelectField)
        assert isinstance(form.submit, SubmitField)

        expected_choices = [
            ('Laptop'),
            ('Desktop'),
            ('Keyboard'),
            ('Mouse'),
            ('Monitor'),
            ('Headset'),
            ('Printer'),
            ('Mobile'),
            ('Tablet'),
            ('Server')
        ]

        assert form.category.choices == expected_choices


def test_customer_form(app):
    with app.app_context():
        form = CustomerForm(name="Test Customer")
        assert form.validate() == True


def test_incorrect_customer_form(app):
    with app.app_context():
        form = CustomerForm()
        assert form.validate() == False


def test_manufacturer_form(app):
    with app.app_context():
        form = ManufacturerForm(name="Test Manufacturer")
        assert form.validate() == True


def test_incorrect_manufacturer_form(app):
    with app.app_context():
        form = ManufacturerForm()
        assert form.validate() == False


if __name__ == '__main__':
    pytest.main()
