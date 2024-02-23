from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

# The following code defines User, Asset, Customer, and Manufacturer classes, and ties them to individual database tables. Primary and foreign keys are assigned to the ID fields for each table to establish relationships between them, and the nullable function is used to ensure that a field has to have data present. Using the unique function for the username field within the User class ensures that a user cannot register within the application using a username that is already present in the database (this is carried out in the login route in routes.py by querying the User class upon form submission)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='regular')
    assets = db.relationship('Asset', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(
        db.Integer, db.ForeignKey('customer.id'), nullable=True)
    manufacturer_id = db.Column(
        db.Integer, db.ForeignKey('manufacturer.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Asset('{self.category}', '{self.timestamp}')"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    assets = db.relationship('Asset', backref='customer', lazy=True)

    def __repr__(self):
        return f"Customer('{self.name}')"


class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    assets = db.relationship('Asset', backref='manufacturer', lazy=True)

    def __repr__(self):
        return f"Manufacturer('{self.name}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
