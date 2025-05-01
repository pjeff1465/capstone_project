import pytest
from app.flask_entry import create_app
from app.extensions import db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_signup_page_loads(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_user_signup(client):
    response = client.post('/signup', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data 

def test_login_valid_user(client, app):
    with app.app_context():
        from app.models import User
        from werkzeug.security import generate_password_hash
        test_user = User(email='test@example.com', password=generate_password_hash('password123'))
        db.session.add(test_user)
        db.session.commit()

    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_login_invalid_user(client):
    response = client.post('/login', data={
        'email': 'invalid@example.com',
        'password': 'invalidpass'
    }, follow_redirects=True)

    assert b"Incorrect" in response.data