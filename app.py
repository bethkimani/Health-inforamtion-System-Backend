from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="Health Information System API",
    description="API for managing clients, health programs, appointments, suppliers, and dashboard metrics",
    version="1.0"
)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    from routes.auth import auth_ns
    from routes.client import client_ns
    from routes.program import program_ns
    from routes.appointment import appointment_ns
    from routes.supplier import supplier_ns
    from routes.dashboard import dashboard_ns
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(client_ns, path='/api/clients')
    api.add_namespace(program_ns, path='/api/programs')
    api.add_namespace(appointment_ns, path='/api/appointments')
    api.add_namespace(supplier_ns, path='/api/suppliers')
    api.add_namespace(dashboard_ns, path='/api/dashboard')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)