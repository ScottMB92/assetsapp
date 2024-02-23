import pytest
from app import create_app, db
from app.models import User, Asset, Customer, Manufacturer

# The following code disables CSRF protection to enable the Pytest unit tests that follow to run, which check the database models to ensure that data can be added to each of the tables (User, Asset, Customer and Manufacturer). The remove_test_data function is then run at the end to delete all of the test data created during the tests, whilst leaving the pre-existing data within the database intact


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()

        reset_db(app)


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


def remove_test_data(app):
    with app.app_context():
        db.session.query(User).filter_by(username='Test User').delete()
        db.session.query(User).filter_by(
            username='Test Asset Form User').delete()
        db.session.query(Asset).filter_by(category='Test Category').delete()
        db.session.query(Customer).filter_by(
            name='Test Asset Form Customer').delete()
        db.session.query(Manufacturer).filter_by(
            name='Test Asset Form Manufacturer').delete()
        db.session.query(Customer).filter_by(name='Test Customer').delete()
        db.session.query(Manufacturer).filter_by(
            name='Test Manufacturer').delete()
        db.session.commit()


def test_create_user(client):
    with client.application.app_context():
        user = User(username='Test User', password='testpassword')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'Test User'
        assert user.password == 'testpassword'


def test_create_asset(client):
    with client.application.app_context():

        user = User(username='Test Asset Form User',
                    password='testassetpassword')
        db.session.add(user)
        db.session.commit()

        customer = Customer(name='Test Asset Form Customer')
        manufacturer = Manufacturer(name='Test Asset Form Manufacturer')
        db.session.add_all([customer, manufacturer])
        db.session.commit()

        category = 'Test Category'
        comments = 'Test Comments'
        customer_id = customer.id
        manufacturer_id = manufacturer.id

        asset = Asset(category=category, comments=comments, user_id=user.id,
                      customer_id=customer_id, manufacturer_id=manufacturer_id)
        db.session.add(asset)
        db.session.commit()


def test_create_customer(client):
    with client.application.app_context():
        customer = Customer(name='Test Customer')
        db.session.add(customer)
        db.session.commit()

        assert customer.id is not None
        assert customer.name == 'Test Customer'


def test_create_manufacturer(client):
    with client.application.app_context():
        manufacturer = Manufacturer(name='Test Manufacturer')
        db.session.add(manufacturer)
        db.session.commit()

        assert manufacturer.id is not None
        assert manufacturer.name == 'Test Manufacturer'


def reset_db(app):
    remove_test_data(app)

    with app.app_context():
        assert db.session.query(User).filter_by(
            username='Test User').count() == 0
        assert db.session.query(User).filter_by(
            username='Test Asset Form User').count() == 0
        assert db.session.query(Asset).filter_by(
            category='Test Category').count() == 0
        assert db.session.query(Customer).filter_by(
            name='Test Asset Form Customer').count() == 0
        assert db.session.query(Manufacturer).filter_by(
            name='Test Asset Form Manufacturer').count() == 0
        assert db.session.query(Customer).filter_by(
            name='Test Customer').count() == 0
        assert db.session.query(Manufacturer).filter_by(
            name='Test Manufacturer').count() == 0


if __name__ == '__main__':
    pytest.main()
