import pytest
from app import db, create_app
from models.client import Client
from models.program import Program

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
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password',
        'role': 'user'
    })
    print("Register response:", response.json)  # Debug output
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password'
    })
    print("Login response:", response.json)  # Debug output
    return response.json['access_token']

def test_create_appointment(client, token):
    with client.application.app_context():
        client_obj = Client(first_name='John', last_name='Doe', email='john.doe@example.com')
        program = Program(name='TB Program', description='Tuberculosis treatment')
        db.session.add(client_obj)
        db.session.add(program)
        db.session.commit()
        client_id = Client.query.first().id
        program_id = Program.query.first().id
        print("Clients:", [(c.id, c.email) for c in Client.query.all()])
        print("Programs:", [(p.id, p.name) for p in Program.query.all()])
    response = client.post('/api/appointments', json={
        'client_id': client_id,
        'program_id': program_id,
        'status': 'Pending'
    }, headers={'Authorization': f'Bearer {token}'})
    print("Response:", response.json)
    assert response.status_code == 201
    assert response.json['status'] == 'Pending'