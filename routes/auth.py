# auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models.user import User
from models import db
import logging

# Configure logging to help debug issues
logging.basicConfig(level=logging.DEBUG)

# Create the auth blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handle user login by verifying email and password, and return a JWT access token.
    """
    try:
        # Parse the JSON request body
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Missing JSON in request'}), 400

        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            logging.debug(f"Missing email or password: email={email}")
            return jsonify({'message': 'Email and password are required'}), 400

        logging.debug(f"Login attempt with email: {email}")

        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            logging.debug("User not found")
            return jsonify({'message': 'Invalid credentials'}), 401

        # Verify the password
        if not user.check_password(password):
            logging.debug("Password check failed")
            return jsonify({'message': 'Invalid credentials'}), 401

        # Generate a JWT access token
        access_token = create_access_token(identity=user.id)
        logging.debug("Access token created successfully")

        return jsonify({
            'access_token': access_token,
            'user': {
                'email': user.email,
                'role': user.role
            }
        }), 200

    except Exception as e:
        # Log the error with full stack trace for debugging
        logging.error(f"Error during login: {str(e)}", exc_info=True)
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register_user():
    """
    Register a new user (requires JWT authentication).
    """
    try:
        # Parse the JSON request body
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Missing JSON in request'}), 400

        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'Administrator')

        # Validate input
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 400

        # Create a new user
        user = User(email=email, role=role)
        user.set_password(password)

        # Save to the database
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        # Log the error with full stack trace for debugging
        logging.error(f"Error during registration: {str(e)}", exc_info=True)
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500