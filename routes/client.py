from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.client import Client
from models import db
from datetime import datetime

client_bp = Blueprint('client', __name__)

@client_bp.route('/clients', methods=['GET'])
@jwt_required()
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        'id': c.id,
        'first_name': c.first_name,
        'last_name': c.last_name,
        'dob': c.dob.isoformat(),
        'gender': c.gender,
        'email': c.email,
        'phone_number': c.phone_number,
        'programs': [p.name for p in c.programs]
    } for c in clients]), 200

@client_bp.route('/clients', methods=['POST'])
@jwt_required()
def add_client():
    data = request.get_json()
    client = Client(
        id=data['id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
        gender=data['gender'],
        email=data['email'],
        phone_number=data['phone_number']
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({'message': 'Client added successfully'}), 201