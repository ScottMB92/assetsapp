from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.models import User

# Lines 9 to 30 utilise the Flask WTForms library to define the class for the registration form that appears on register.html. All three fields of the form (username, password, and confirm password) are validated to ensure that data is present in the username and password fields. It is also checked that the username has a minimum of 3 characters entered and a maximum of 20 characters, and that the confirmed password matches what is entered into the initial password field. It also ensures that passwords contain at least one digit, one lowercase letter, one uppercase letter, and one special character. The validate_username function checks the database to ensure that the username entered is not already present, and if it is, a validation error occurs. The validate_password function checks that the password entered is at least 8 characters long, and if it is not, a validation error occurs


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[
                             DataRequired(),
                             Length(min=8),
                             Regexp(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$',
                                    message="Password must contain a digit, lowercase, uppercase, and special character.")
                             ])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError(
                'Password must be at least 8 characters long.')

# Lines 35 to 39 utilise the Flask WTForms library to define the class for the login form that appears on login.html. Both the username and password fields are validated to ensure that data is present in both, and that the username has a minimum of 2 characters


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Lines 44 to 64 utilise the Flask WTForms library to define the class for the asset creation form that appears on assets.html. The category choices are based on the ones defined in the list below, the comments field is a free text field that may or may not require data, whilst the customer and manufacturer fields pull data from the database by finding the ID of the corresponding customer/manufacturer


class AssetForm(FlaskForm):
    category_choices = [
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

    category = SelectField(
        'Category', choices=category_choices, validators=[DataRequired()])
    comments = TextAreaField('Comments')
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])
    manufacturer = SelectField(
        'Manufacturer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Asset')

# Lines 69 to 71 utilise the Flask WTForms library to define the class for the customer creation form that appears on customers.html. The name field is validated to ensure that data is present before it can be submitted


class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Customer')

# Lines 76 to 78 utilise the Flask WTForms library to define the class for the manufacturer creation form that appears on manufacturers.html. The name field is validated to ensure that data is present before it can be submitted


class ManufacturerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Manufacturer')
