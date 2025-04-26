# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db
from routes import init_routes

app = Flask(__name__)
app.config.from_object(Config)

# Define allowed origins
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Your frontend URL
]

# Initialize CORS with specific configuration
CORS(app, resources={
    r"/api/*": {  # Apply CORS to all /api routes
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"],
    }
}, supports_credentials=True)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Register routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)