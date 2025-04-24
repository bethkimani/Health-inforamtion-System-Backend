import pytest
from app import app, db
from models.client import Client

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_client(client):
    response = client.post('/api/clients', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+1234567890'
    })
    assert response.status_code == 201
    assert response.json['name'] == 'John Doe'