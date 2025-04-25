import pytest
from app import create_app, db
from models.client import Client
from models.user import User
from flask_jwt_extended import create_access_token

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

@pytest.fixture
def token(app):
    with app.app_context():
        user = User(email='test@doctor.com', role='doctor')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return create_access_token(identity=user.id)

def test_create_client(client, token):
    response = client.post('/api/clients', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'dob': '1990-01-01',
        'gender': 'Male',
        'status': 'triage'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['first_name'] == 'John'

def test_create_client_invalid_data(client, token):
    response = client.post('/api/clients', json={
        'first_name': '',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert 'first_name' in response.json['message'].lower()

def test_get_clients(client, token):
    with client.application.app_context():
        client_obj = Client(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            status='triage'
        )
        db.session.add(client_obj)
        db.session.commit()
    response = client.get('/api/clients', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_client_by_id(client, token):
    with client.application.app_context():
        client_obj = Client(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            status='triage'
        )
        db.session.add(client_obj)
        db.session.commit()
    response = client.get('/api/clients/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['first_name'] == 'John'

def test_get_client_not_found(client, token):
    response = client.get('/api/clients/999', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.json['message'] == 'Client not found'

def test_update_client(client, token):
    with client.application.app_context():
        client_obj = Client(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            status='triage'
        )
        db.session.add(client_obj)
        db.session.commit()
    response = client.put('/api/clients/1', json={
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'status': 'lab'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['first_name'] == 'Jane'

def test_update_client_not_found(client, token):
    response = client.put('/api/clients/999', json={
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.json['message'] == 'Client not found'

def test_delete_client(client, token):
    with client.application.app_context():
        client_obj = Client(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            status='triage'
        )
        db.session.add(client_obj)
        db.session.commit()
    response = client.delete('/api/clients/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Client deleted'

def test_delete_client_not_found(client, token):
    response = client.delete('/api/clients/999', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.json['message'] == 'Client not found'