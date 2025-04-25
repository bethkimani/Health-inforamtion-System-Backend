import pytest
from app import create_app, db
from models.client import Client

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

@pytest.fixture
def token(client):
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password',
        'role': 'user'
    })
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password'
    })
    return response.json['access_token']

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
    print("Create client response:", response.json)
    assert response.status_code == 201

def test_create_client_invalid_data(client, token):
    response = client.post('/api/clients', json={
        'first_name': '',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    }, headers={'Authorization': f'Bearer {token}'})
    print("Create client invalid data response:", response.json)
    assert response.status_code == 400

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
    print("Get clients response:", response.json)
    assert response.status_code == 200

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
    print("Get client by ID response:", response.json)
    assert response.status_code == 200

def test_get_client_not_found(client, token):
    response = client.get('/api/clients/999', headers={'Authorization': f'Bearer {token}'})
    print("Get client not found response:", response.json)
    assert response.status_code == 404

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
    print("Update client response:", response.json)
    assert response.status_code == 200

def test_update_client_not_found(client, token):
    response = client.put('/api/clients/999', json={
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com'
    }, headers={'Authorization': f'Bearer {token}'})
    print("Update client not found response:", response.json)
    assert response.status_code == 404

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
    print("Delete client response:", response.json)
    assert response.status_code == 200

def test_delete_client_not_found(client, token):
    response = client.delete('/api/clients/999', headers={'Authorization': f'Bearer {token}'})
    print("Delete client not found response:", response.json)
    assert response.status_code == 404