import pytest
from app import create_app, db
from models.supplier import Supplier
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

def test_create_supplier(client, token):
    response = client.post('/api/suppliers', json={
        'name': 'MedSupply',
        'contact_info': 'contact@medsupply.com',
        'contract_details': 'Annual contract'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['name'] == 'MedSupply'

def test_get_suppliers(client, token):
    with client.application.app_context():
        supplier = Supplier(name='MedSupply', contact_info='contact@medsupply.com')
        db.session.add(supplier)
        db.session.commit()
    response = client.get('/api/suppliers', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.json) == 1

def test_supplier_with_empty_name(client, token):
    response = client.post('/api/suppliers', json={
        'name': '',
        'contact_info': 'contact@medsupply.com'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert 'name' in response.json['message'].lower()