from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

# Lines 8 to 14 utilise the Flask WTForms library to define the class for the registration form that appears on register.html. All three fields of the form (username, password, and confirm password) are validated to ensure that data is present in the username and password fields. It is also checked that the username has a minimum of 2 characters entered and a maximum of 20 characters, and that the confirmed password matches what is entered into the initial password field


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Lines 19 to 23 utilise the Flask WTForms library to define the class for the login form that appears on login.html. Both the username and password fields are validated to ensure that data is present in both, and that the username has a minimum of 2 characters


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Lines 28 to 47 utilise the Flask WTForms library to define the class for the asset creation form that appears on assets.html. The category choices are based on the ones defined in the list below, the comments field is a free text field that may or may not require data, whilst the customer and manufacturer fields pull data from the database by finding the ID of the corresponding customer/manufacturer


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

# Lines 52 to 54 utilise the Flask WTForms library to define the class for the customer creation form that appears on customers.html. The name field is validated to ensure that data is present before it can be submitted


class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Customer')

# Lines 59 to 61 utilise the Flask WTForms library to define the class for the manufacturer creation form that appears on manufacturers.html. The name field is validated to ensure that data is present before it can be submitted


class ManufacturerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Manufacturer')
