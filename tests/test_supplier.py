import pytest
from app import create_app, db
from models.supplier import Supplier

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

def test_create_supplier(client, token):
    response = client.post('/api/suppliers', json={
        'name': 'MedSupply',
        'contact_info': 'contact@medsupply.com',
        'contract_details': 'Annual contract'
    }, headers={'Authorization': f'Bearer {token}'})
    print("Create supplier response:", response.json)
    assert response.status_code == 201

def test_get_suppliers(client, token):
    with client.application.app_context():
        supplier = Supplier(name='MedSupply', contact_info='contact@medsupply.com')
        db.session.add(supplier)
        db.session.commit()
    response = client.get('/api/suppliers', headers={'Authorization': f'Bearer {token}'})
    print("Get suppliers response:", response.json)
    assert response.status_code == 200

def test_supplier_with_empty_name(client, token):
    response = client.post('/api/suppliers', json={
        'name': '',
        'contact_info': 'contact@medsupply.com'
    }, headers={'Authorization': f'Bearer {token}'})
    print("Supplier empty name response:", response.json)
    assert response.status_code == 400