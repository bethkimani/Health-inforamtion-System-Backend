import pytest
from app import create_app, db
from models.user import User
from models.client import Client
from models.program import Program
from models.appointment import Appointment
from flask_jwt_extended import create_access_token
from datetime import datetime

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

def test_create_appointment(client, token):
    client_data = Client(first_name='John', last_name='Doe', email='john.doe@example.com')
    program = Program(name='TB Program', description='Tuberculosis treatment')
    db.session.add(client_data)
    db.session.add(program)
    db.session.commit()

    response = client.post('/api/appointments', json={
        'client_id': 1,
        'program_id': 1,
        'requested_at': datetime.utcnow().isoformat()
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['message'] == 'Appointment created successfully'

def test_get_appointments(client, token):
    client_data = Client(first_name='John', last_name='Doe', email='john.doe@example.com')
    program = Program(name='TB Program', description='Tuberculosis treatment')
    appointment = Appointment(client_id=1, program_id=1, status='Pending')
    db.session.add(client_data)
    db.session.add(program)
    db.session.add(appointment)
    db.session.commit()

    response = client.get('/api/appointments', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['client_name'] == 'John Doe'

def test_update_appointment_status(client, token):
    client_data = Client(first_name='John', last_name='Doe', email='john.doe@example.com')
    program = Program(name='TB Program', description='Tuberculosis treatment')
    appointment = Appointment(client_id=1, program_id=1, status='Pending')
    db.session.add(client_data)
    db.session.add(program)
    db.session.add(appointment)
    db.session.commit()

    response = client.put('/api/appointments/1/status', json={
        'status': 'Approved'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Appointment status updated to Approved'