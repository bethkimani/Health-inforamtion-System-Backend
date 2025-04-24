from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.program import Program, db

program_routes = Blueprint('program_routes', __name__)

@program_routes.route('/programs', methods=['POST'])
@jwt_required()
def create_program():
    data = request.get_json()
    new_program = Program(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(new_program)
    db.session.commit()
    return jsonify(new_program.to_dict()), 201

@program_routes.route('/programs', methods=['GET'])
@jwt_required()
def get_programs():
    programs = Program.query.all()
    return jsonify([program.to_dict() for program in programs]), 200