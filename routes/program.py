from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.program import Program
from models import db

program_bp = Blueprint('program', __name__)

@program_bp.route('/programs', methods=['GET'])
@jwt_required()
def get_programs():
    programs = Program.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description
    } for p in programs]), 200

@program_bp.route('/programs', methods=['POST'])
@jwt_required()
def add_program():
    data = request.get_json()
    program = Program(
        id=data['id'],
        name=data['name'],
        description=data['description']
    )
    db.session.add(program)
    db.session.commit()
    return jsonify({'message': 'Program added successfully'}), 201

@program_bp.route('/programs/<id>', methods=['DELETE'])
@jwt_required()
def delete_program(id):
    program = Program.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    return jsonify({'message': 'Program deleted successfully'}), 200