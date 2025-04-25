import pytest
from app import create_app, db
from models.user import User
from models.client import Client
from models.program import Program
from models.appointment import Appointment
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

def test_dashboard_metrics(client, token):
    client1 = Client(first_name='John', last_name='Doe', email='john.doe@example.com', status='triage')
    client2 = Client(first_name='Jane', last_name='Smith', email='jane.smith@example.com', status='lab')
    program = Program(name='TB Program', description='Tuberculosis treatment')
    appointment = Appointment(client_id=1, program_id=1, status='Pending')
    db.session.add(client1)
    db.session.add(client2)
    db.session.add(program)
    db.session.add(appointment)
    db.session.commit()

    response = client.get('/api/dashboard/metrics', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['total_patients'] == 2
    assert response.json['appointment_status']['Pending'] == 1
    assert response.json['appointment_status']['Approved'] == 0
    assert response.json['appointment_status']['Completed'] == 0
    assert response.json['status_counts']['triage'] == 1
    assert response.json['status_counts']['lab'] == 1
    assert response.json['status_counts']['pharmacy'] == 0
    assert len(response.json['recent_appointments']) == 1
    assert response.json['recent_appointments'][0]['client_name'] == 'John Doe'