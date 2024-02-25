from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, Flask
from flask_login import login_user, login_required, current_user, logout_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, limiter
from app.models import User, Asset, Customer, Manufacturer
from app.forms import RegistrationForm, LoginForm, AssetForm, CustomerForm, ManufacturerForm
import logging

main = Blueprint('main', __name__)


app = Flask(__name__)
csrf = CSRFProtect(app)

logging.basicConfig(filename='app.log', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())


@main.errorhandler(429)
def ratelimit_handler(e):
    form = LoginForm()
    flash("Too many requests, you have been locked out for one minute.", 'danger')
    return render_template('login.html', form=form), 429

# Lines 29 to 36 ensure that the index.html page is loaded when accessing the root URL, which occurs when the app starts running on the server


@main.route('/')
def index():
    current_app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Strict'
    )
    return render_template('index.html')


# Lines 42 to 74 ensure that when the register.html page is accessed, the registration form is retrieved. When the user submits the form, validation takes place to query the User class and check the database to make sure a user cannot register with a username that has already been used, and if that username does already exist then a warning message will display to ask the user to choose a different one. It will also check to make sure that the user doesn't use the same information in the username and password fields, if they do then a warning message will display saying that the data in these fields must be different. Another check follows to ensure that the data entered into the password and confirm password fields is the same, if it doesn't then the user will be informed that the information must match. Following this, the password chosen is hashed using the Werkzeug library's scrypt method to encrypt the password within the database so that it is not stored in plain text. Then, the user is automatically set as a regular user so that they can perform CRU (Create, Read, Update) operations, but not CRUD (Create, Read, Update, Delete) operations, which are reserved for admin users. The new user's data is committed to the database, and they are redirected to the login page where a flash message informs them that registration was successful


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(
            username=form.username.data).first()
        if existing_user:
            flash(
                'Username is already taken. Please choose a different username.', 'danger')
            logging.warning(
                'Attempted to register with existing username: %s', form.username.data)
        elif form.username.data == form.password.data:
            flash('Username and password must be different.', 'danger')
        elif form.password.data != form.confirm_password.data:
            flash('Password and confirm password must match.', 'danger')
        else:
            hashed_password = generate_password_hash(
                form.password.data, method='scrypt')
            new_user = User(username=form.username.data,
                            password=hashed_password, role='regular')
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in below', 'success')
            logging.info('User registered successfully: %s',
                         form.username.data)
            return redirect(url_for('main.login'))

    for _, errors in form.errors.items():
        for error in errors:
            flash(error, 'danger')
            logging.error(error)

    return render_template('register.html', form=form)


# Lines 80 to 95 ensure that when the register.html page is accessed, the login form is retrieved. When the user attempts to login with their details, validation takes place to check that the username and hashed password match an entry in the user table within the database. If an incorrect username or password is entered amd submitted, they will be unable to login and will see a flash message informing them that their details are incorrect. If the username and password are correct and a match, the user is redirected to the homepage and informed of their successful login


@main.route('/login', methods=['GET', 'POST'])
@limiter.limit("5/minute", key_func=lambda: request.remote_addr)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Successfully logged in', 'success')
            logging.info('User logged in successfully: %s', form.username.data)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
            logging.warning(
                'Invalid login attempt with username: %s', form.username.data)
    return render_template('login.html', form=form)


# Lines 101 to 108 ensure that the user is redirected to logout.html when they click on the logout button, upon which they will encounter a dialog box asking if they want to confirm or cancel the logout action. If they confirm the action, the user will be logged out of the application and redirected to the homepage, upon which they will see a flashed message informing them of their successful logout


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('Successfully logged out', 'success')
        return redirect(url_for('main.index'))
    return render_template('logout.html')


# Lines 114 to 133 ensure that when the assets.html page is accessed, the assets form is retrieved. Validation takes place on submission to check that the data in each field matches the database model, and if it does, the new record is committed to the database and a flashed message appears to inform the user of the successful submission


@main.route('/assets', methods=['GET', 'POST'])
@login_required
def assets():
    form = AssetForm()

    form.manufacturer.choices = [(m.id, m.name)
                                 for m in Manufacturer.query.all()]
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]

    if form.validate_on_submit():
        new_asset = Asset(category=form.category.data, comments=form.comments.data, user_id=current_user.id,
                          manufacturer_id=form.manufacturer.data, customer_id=form.customer.data)
        db.session.add(new_asset)
        db.session.commit()
        flash('Asset created', 'success')
        logging.info('New asset created by user: %s', current_user.username)
        return redirect(url_for('main.assets'))

    assets = Asset.query.all()
    return render_template('assets.html', form=form, assets=assets)


# The asset edit route (lines 139 to 171) directs the user to the edit_asset.html page and prepopulates the fields with the data that forms the selected record retrieved from the database. Validation again takes place upon submission, and the user is redirected back to the assets page and informed of the successful edited submission


@main.route('/assets/<int:asset_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)

    form = AssetForm()

    form.customer.choices = [(customer.id, customer.name)
                             for customer in Customer.query.all()]
    form.manufacturer.choices = [(manufacturer.id, manufacturer.name)
                                 for manufacturer in Manufacturer.query.all()]

    if request.method == 'POST':
        if form.validate_on_submit():
            asset.category = form.category.data
            asset.comments = form.comments.data
            asset.customer_id = form.customer.data
            asset.manufacturer_id = form.manufacturer.data
            db.session.commit()
            flash('Asset updated', 'success')
            logging.info('Asset updated by user: %s', current_user.username)
            return redirect(url_for('main.assets'))
        else:
            flash('Form validation failed', 'danger')
            logging.error(
                'Form validation failed for asset edit by user: %s', current_user.username)
    else:
        form.category.data = asset.category
        form.comments.data = asset.comments
        form.customer.data = asset.customer_id
        form.manufacturer.data = asset.manufacturer_id

    return render_template('edit_asset.html', form=form, asset=asset)


# If the user logged in is marked as an admin within the database, the asset delete route (lines 177 to 192) ensures that a dialog box appears that asks the user if they want to confirm deletion of the asset selected or cancel the action which, if confirmed, removes the record from the database and informs the user that deletion was successful. If the user logged in is marked as a regular user within the database, however, then a flashed message appears informing the user that they do not have permission to delete assets


@main.route('/assets/<int:asset_id>/delete', methods=['POST'])
@login_required
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)

    if current_user.role == 'admin':
        db.session.delete(asset)
        db.session.commit()
        flash('Asset deleted', 'success')
        logging.info('Asset deleted by user: %s', current_user.username)
    else:
        flash('You do not have permission to delete this asset.', 'warning')
        logging.warning(
            'User attempted to delete asset without permission: %s', current_user.username)

    return redirect(url_for('main.assets'))


# Lines 198 to 212 ensure that when the customers.html page is accessed, the customers form is retrieved. Validation takes place on submission to check that the data in each field matches the database model, and if it does, the new record is committed to the database and a flashed message appears to inform the user of the successful submission


@main.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    customer_form = CustomerForm()

    if customer_form.validate_on_submit():
        new_customer = Customer(name=customer_form.name.data)
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer created', 'success')
        logging.info('New customer created by user: %s', current_user.username)
        return redirect(url_for('main.customers'))

    customers = Customer.query.all()
    return render_template('customers.html', customers=customers, customer_form=customer_form)


# The customer edit route (lines 218 to 238) directs the user to the edit_customer.html page and prepopulates the fields with the data that forms the selected record retrieved from the database. Validation again takes place upon submission, and the user is redirected back to the edit customer page and informed of the successful edited submission


@main.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_form = CustomerForm()

    if customer_form.validate_on_submit():
        customer.name = customer_form.name.data
        db.session.commit()
        flash('Customer updated', 'success')
        logging.info('Customer updated by user: %s', current_user.username)
        return redirect(url_for('main.customers'))

    elif request.method == 'POST':
        flash('Form validation failed', 'danger')
        logging.error(
            'Form validation failed for customer edit by user: %s', current_user.username)
    else:
        customer_form.name.data = customer.name

    return render_template('edit_customer.html', customer=customer, customer_form=customer_form)


# If the user logged in is marked as an admin within the database, the customer delete route (lines 244 to 259) ensures that a dialog box appears that asks the user if they want to confirm deletion of the customer selected or cancel the action which, if confirmed, removes the record from the database and informs the user that deletion was successful. If the user logged in is marked as a regular user within the database, however, then a flashed message appears informing the user that they do not have permission to delete customers


@main.route('/delete_customer/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if current_user.role == 'admin':
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted', 'success')
        logging.info('Customer deleted by user: %s', current_user.username)
    else:
        flash('You do not have permission to delete this customer.', 'warning')
        logging.warning(
            'User attempted to delete customer without permission: %s', current_user.username)

    return redirect(url_for('main.customers'))


# Lines 265 to 280 ensure that when the manufacturers.html page is accessed, the manufacturers form is retrieved. Validation takes place on submission to check that the data in each field matches the database model, and if it does, the new record is committed to the database and a flashed message appears to inform the user of the successful submission


@main.route('/manufacturers', methods=['GET', 'POST'])
@login_required
def manufacturers():
    manufacturer_form = ManufacturerForm()

    if manufacturer_form.validate_on_submit():
        new_manufacturer = Manufacturer(name=manufacturer_form.name.data)
        db.session.add(new_manufacturer)
        db.session.commit()
        flash('Manufacturer created', 'success')
        logging.info('New manufacturer created by user: %s',
                     current_user.username)
        return redirect(url_for('main.manufacturers'))

    manufacturers = Manufacturer.query.all()
    return render_template('manufacturers.html', manufacturers=manufacturers, manufacturer_form=manufacturer_form)


# The manufacturer edit route (lines 286 to 305) directs the user to the edit_manufacturer.html page and prepopulates the fields with the data that forms the selected record retrieved from the database. Validation again takes place upon submission, and the user is redirected back to the edit manufacturer page and informed of the successful edited submission


@main.route('/edit_manufacturer/<int:manufacturer_id>', methods=['GET', 'POST'])
@login_required
def edit_manufacturer(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
    manufacturer_form = ManufacturerForm()

    if manufacturer_form.validate_on_submit():
        manufacturer.name = manufacturer_form.name.data
        db.session.commit()
        flash('Manufacturer updated', 'success')
        logging.info('Manufacturer updated by user: %s', current_user.username)
        return redirect(url_for('main.manufacturers'))
    elif request.method == 'POST':
        flash('Form validation failed', 'danger')
        logging.error(
            'Form validation failed for manufacturer edit by user: %s', current_user.username)
    else:
        manufacturer_form.name.data = manufacturer.name

    return render_template('edit_manufacturer.html', manufacturer=manufacturer, manufacturer_form=manufacturer_form)


# If the user logged in is marked as an admin within the database, the manufacturer delete route (lines 311 to 326) ensures that a dialog box appears that asks the user if they want to confirm deletion of the manufacturer selected or cancel the action which, if confirmed, removes the record from the database and informs the user that deletion was successful. If the user logged in is marked as a regular user within the database, however, then a flashed message appears informing the user that they do not have permission to delete manufacturers


@main.route('/delete_manufacturer/<int:manufacturer_id>', methods=['POST'])
@login_required
def delete_manufacturer(manufacturer_id):
    manufacturer = Manufacturer.query.get_or_404(manufacturer_id)

    if current_user.role == 'admin':
        db.session.delete(manufacturer)
        db.session.commit()
        flash('Manufacturer deleted', 'success')
        logging.info('Manufacturer deleted by user: %s', current_user.username)
    else:
        flash('You do not have permission to delete this manufacturer.', 'warning')
        logging.warning(
            'User attempted to delete manufacturer without permission: %s', current_user.username)

    return redirect(url_for('main.manufacturers'))
