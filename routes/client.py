from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.client import Client
from models import db
from datetime import datetime
import logging

client_bp = Blueprint('client', __name__, url_prefix='/api')

@client_bp.route('/clients', methods=['GET', 'OPTIONS'])
# @jwt_required()  # Temporarily disable
def get_clients():
    try:
        clients = Client.query.all()
        clients_data = []
        for client in clients:
            client_data = {
                'id': client.id,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'dob': client.dob.isoformat() if client.dob else None,
                'gender': client.gender,
                'email': client.email,
                'phone_number': client.phone_number,
                'programs': [p.name for p in client.programs] if client.programs else []
            }
            clients_data.append(client_data)
        return jsonify({'success': True, 'data': clients_data}), 200
    except Exception as e:
        logging.error(f"Error fetching clients: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@client_bp.route('/clients', methods=['POST', 'OPTIONS'])
# @jwt_required()  # Temporarily disable
def add_client():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        required_fields = ['id', 'first_name', 'last_name', 'dob', 'gender', 'email', 'phone_number']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing fields: {", ".join(missing_fields)}'
            }), 400

        if Client.query.get(data['id']):
            return jsonify({'success': False, 'message': 'Client ID already exists'}), 400

        dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()

        new_client = Client(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=dob,
            gender=data['gender'],
            email=data['email'],
            phone_number=data['phone_number']
        )

        db.session.add(new_client)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Client added successfully',
            'data': {
                'id': new_client.id,
                'first_name': new_client.first_name,
                'last_name': new_client.last_name,
                'dob': new_client.dob.isoformat(),
                'gender': new_client.gender,
                'email': new_client.email,
                'phone_number': new_client.phone_number
            }
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'message': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500