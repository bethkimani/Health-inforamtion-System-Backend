from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db
from routes import init_routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Configure CORS with detailed logging
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Authorization"]
    }
})

# Log CORS preflight requests
@app.before_request
def before_request():
    if request.method == "OPTIONS":
        app.logger.debug("Handling CORS preflight request")
    app.logger.debug(f"Incoming request: {request.method} {request.path}")
    app.logger.debug(f"Headers: {dict(request.headers)}")
    app.logger.debug(f"Body: {request.get_data()}")

# Register routes
init_routes(app)

# Handle JWT errors
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'success': False,
        'message': 'Invalid token',
        'error': 'invalid_token'
    }), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'success': False,
        'message': 'Token has expired',
        'error': 'token_expired'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'success': False,
        'message': 'Request does not contain a valid token',
        'error': 'authorization_required'
    }), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)