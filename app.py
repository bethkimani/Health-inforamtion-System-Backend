from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from config import Config
from dotenv import load_dotenv
import os
from werkzeug.exceptions import HTTPException
import logging

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

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Ensure tokens are read from headers
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    @api.errorhandler(Exception)
    def handle_unprocessable_entity(error):
        logger.error(f"Error caught: {str(error)}", exc_info=True)  # Log full error
        if isinstance(error, HTTPException) and error.code in [400, 401, 404]:
            return {'message': str(error.description), 'errors': {}}, error.code
        return {'message': str(error), 'errors': getattr(error, 'data', {}).get('messages', {})}, 422

    from models.user import User
    from models.supplier import Supplier
    from models.program import Program
    from models.enrollment import Enrollment
    from models.client import Client
    from models.appointment import Appointment

    try:
        from routes.auth import auth_ns
        from routes.client import client_ns
        from routes.program import program_ns
        from routes.appointment import appointment_ns
        from routes.supplier import supplier_ns
        from routes.dashboard import dashboard_ns
    except ImportError as e:
        logger.error(f"ImportError: {e}")
        raise

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