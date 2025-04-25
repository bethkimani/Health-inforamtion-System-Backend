import pytest
from app import create_app, db
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

def test_create_program(client, token):
    response = client.post('/api/programs', json={
        'name': 'TB Program',
        'description': 'Tuberculosis treatment'
    }, headers={'Authorization': f'Bearer {token}'})
    print("Create program response:", response.json)
    assert response.status_code == 201

def test_get_programs(client, token):
    with client.application.app_context():
        program = Program(name='TB Program', description='Tuberculosis treatment')
        db.session.add(program)
        db.session.commit()
    response = client.get('/api/programs', headers={'Authorization': f'Bearer {token}'})
    print("Get programs response:", response.json)
    assert response.status_code == 200