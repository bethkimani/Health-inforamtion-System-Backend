import pytest
from app import create_app, db
from models.program import Program
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

def test_create_program(client, token):
    response = client.post('/api/programs', json={
        'name': 'TB Program',
        'description': 'Tuberculosis treatment'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert response.json['name'] == 'TB Program'

def test_get_programs(client, token):
    program = Program(name='TB Program', description='Tuberculosis treatment')
    db.session.add(program)
    db.session.commit()
    response = client.get('/api/programs', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert len(response.json) == 1