import pytest
from app import create_app, db
from app.models import User

# The following code disables CSRF protection to enable the Pytest unit tests that follow to run, which check the routes for the various pages that comprise the application


@pytest.fixture(scope="module")
def client(request):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()

    def remove_test_data():
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            if user:
                db.session.delete(user)
                db.session.commit()

    request.addfinalizer(remove_test_data)

    yield client


def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200

    response = client.post('/register', data=dict(
        username='testuser',
        password='testpassword',
        confirm_password='testpassword'
    ), follow_redirects=True)

    assert b'Registration successful. Please log in below' in response.data


def test_login(client):
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    assert b'Successfully logged in' in response.data


def test_assets(client):
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = client.get('/assets')
    assert response.status_code == 200
    assert b'Asset Management' in response.data


def test_edit_asset(client):
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = client.get('/assets/1/edit')
    assert response.status_code == 200
    assert b'Edit Asset' in response.data


def test_customers(client):
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = client.get('/customers')
    assert response.status_code == 200
    assert b'Customer Management' in response.data


def test_edit_customer(client):
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = client.get('/edit_customer/1')
    assert response.status_code == 200
    assert b'Edit Customer' in response.data


def test_manufacturers(client):
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = client.get('/manufacturers')
    assert response.status_code == 200
    assert b'Manufacturer Management' in response.data


def test_edit_manufacturer(client):
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    response = client.get('/edit_manufacturer/1')
    assert response.status_code == 200
    assert b'Edit Manufacturer' in response.data


if __name__ == '__main__':
    pytest.main()
