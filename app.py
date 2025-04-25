# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="Health Information System API",
    description="API for managing clients, health programs, appointments, suppliers, and dashboard metrics",
    version="1.0",
    validate=True
)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    # Custom error handler for validation errors
    @api.errorhandler(Exception)
    def handle_unprocessable_entity(error):
        return {'message': str(error), 'errors': getattr(error, 'data', {}).get('messages', {})}, 422

    # Import models
    from models.user import User
    from models.supplier import Supplier
    from models.program import Program
    from models.enrollment import Enrollment
    from models.client import Client
    from models.appointment import Appointment

    # Import namespaces
    try:
        from routes.auth import auth_ns
        from routes.client import client_ns
        from routes.program import program_ns
        from routes.appointment import appointment_ns
        # Temporarily comment out unused namespaces
        # from routes.supplier import supplier_ns
        # from routes.dashboard import dashboard_ns
    except ImportError as e:
        print(f"ImportError: {e}")
        raise

    # Register namespaces
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(client_ns, path='/api/clients')
    api.add_namespace(program_ns, path='/api/programs')
    api.add_namespace(appointment_ns, path='/api/appointments')
    # api.add_namespace(supplier_ns, path='/api/suppliers')
    # api.add_namespace(dashboard_ns, path='/api/dashboard')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
