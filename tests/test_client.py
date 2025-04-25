import pytest
from app import create_app, db
from models.user import User
from models.client import Client
from models.program import Program
from models.enrollment import Enrollment
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

def test_register_client(client, token):
    response = client.post('/api/clients', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'dob': '1990-01-01',
        'gender': 'Male'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['message'] == 'Client registered successfully'

def test_get_client(client, token):
    client_data = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890',
        dob='1990-01-01',
        gender='Male'
    )
    db.session.add(client_data)
    db.session.commit()

    response = client.get('/api/clients/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['email'] == 'john.doe@example.com'

def test_enroll_client(client, token):
    client_data = Client(first_name='John', last_name='Doe', email='john.doe@example.com')
    program = Program(name='TB Program', description='Tuberculosis treatment')
    db.session.add(client_data)
    db.session.add(program)
    db.session.commit()

    response = client.post('/api/clients/enroll', json={
        'client_id': 1,
        'program_id': 1
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['message'] == 'Client enrolled successfully'