import pytest
from app import create_app, db
from models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    response = client.post('/api/auth/register', json={
        'email': 'test@doctor.com',
        'password': 'password123',
        'role': 'doctor',
        'first_name': 'John',
        'last_name': 'Doe'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

def test_login_user(client):
    user = User(email='test@doctor.com', role='doctor', first_name='John', last_name='Doe')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/login', json={
        'email': 'test@doctor.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert response.json['user']['email'] == 'test@doctor.com'

def test_get_profile(client):
    user = User(email='test@doctor.com', role='doctor', first_name='John', last_name='Doe')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    login_response = client.post('/api/auth/login', json={
        'email': 'test@doctor.com',
        'password': 'password123'
    })
    token = login_response.json['access_token']

    response = client.get('/api/auth/profile', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['email'] == 'test@doctor.com'
    assert response.json['first_name'] == 'John'