import pytest
from app import create_app, db
from models.user import User

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'email': 'test@doctor.com',
        'password': 'password',
        'role': 'doctor'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

def test_login(client):
    client.post('/api/auth/register', json={
        'email': 'test@doctor.com',
        'password': 'password',
        'role': 'doctor'
    })
    response = client.post('/api/auth/login', json={
        'email': 'test@doctor.com',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(client):
    response = client.post('/api/auth/login', json={
        'email': 'test@doctor.com',
        'password': 'wrongpassword'
    })
    print("Login invalid credentials response:", response.json)  # Debug output
    assert response.status_code == 401