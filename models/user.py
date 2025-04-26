# models/user.py (Updated)
from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Increased length to accommodate hash
    role = db.Column(db.String(50), nullable=False, default='Administrator')

    def set_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')  # Using pbkdf2:sha256 for reliability
        if not self.password_hash.startswith('pbkdf2:sha256'):
            raise ValueError("Failed to generate a valid password hash")

    def check_password(self, password):
        if not self.password_hash:
            raise ValueError("Password hash is not set for this user")
        return check_password_hash(self.password_hash, password)