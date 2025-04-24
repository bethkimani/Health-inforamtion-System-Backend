from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models.client import db
from routes.client_routes import client_routes
from routes.program_routes import program_routes

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(client_routes, url_prefix='/api')
app.register_blueprint(program_routes, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)