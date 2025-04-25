import pytest
from app import create_app, db
from models.user import User
from models.supplier import Supplier
from flask_jwt_extended import create_access_token
from datetime import date

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
        'name': 'MediSupply Co.',
        'email': 'contact@medisupply.com',
        'phone': '+254 712 345 678',
        'status': True,
        'contract_start_date': '2025-01-01',
        'contract_end_date': '2026-01-01'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['message'] == 'Supplier created successfully'

def test_get_supplier(client, token):
    supplier = Supplier(
        name='MediSupply Co.',
        email='contact@medisupply.com',
        phone='+254 712 345 678',
        status=True
    )
    db.session.add(supplier)
    db.session.commit()

    response = client.get('/api/suppliers/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'MediSupply Co.'

def test_delete_supplier(client, token):
    supplier = Supplier(
        name='MediSupply Co.',
        email='contact@medisupply.com',
        phone='+254 712 345 678',
        status=True
    )
    db.session.add(supplier)
    db.session.commit()

    response = client.delete('/api/suppliers/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Supplier deleted successfully'