from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.client import Client, db
from models.program import Program

client_routes = Blueprint('client_routes', __name__)

@client_routes.route('/clients', methods=['POST'])
@jwt_required()
def register_client():
    data = request.get_json()
    new_client = Client(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify(new_client.to_dict()), 201

@client_routes.route('/clients/<int:id>', methods=['GET'])
@jwt_required()
def get_client(id):
    client = Client.query.get_or_404(id)
    return jsonify(client.to_dict()), 200

@client_routes.route('/clients/search', methods=['GET'])
@jwt_required()
def search_client():
    query = request.args.get('query', '')
    clients = Client.query.filter(Client.name.ilike(f'%{query}%')).all()
    return jsonify([client.to_dict() for client in clients]), 200

@client_routes.route('/clients/<int:client_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_client(client_id):
    data = request.get_json()
    client = Client.query.get_or_404(client_id)
    program = Program.query.get_or_404(data['program_id'])
    client.programs.append(program)
    db.session.commit()
    return jsonify(client.to_dict()), 200