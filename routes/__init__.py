from flask import Blueprint
from .auth import auth_bp
from .client import client_bp
from .program import program_bp
from .appointment import appointment_bp
from .health_record import health_record_bp
from .supplier import supplier_bp
from .team_member import team_member_bp

def init_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(client_bp, url_prefix='/api')
    app.register_blueprint(program_bp, url_prefix='/api')
    app.register_blueprint(appointment_bp, url_prefix='/api')
    app.register_blueprint(health_record_bp, url_prefix='/api')
    app.register_blueprint(supplier_bp, url_prefix='/api')
    app.register_blueprint(team_member_bp, url_prefix='/api')