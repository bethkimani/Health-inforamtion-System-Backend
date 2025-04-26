from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.team_member import TeamMember
from models import db

team_member_bp = Blueprint('team_member', __name__)

@team_member_bp.route('/team', methods=['GET'])
@jwt_required()
def get_team_members():
    members = TeamMember.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'email': m.email,
        'phone_number': m.phone_number,
        'role': m.role
    } for m in members]), 200

@team_member_bp.route('/team', methods=['POST'])
@jwt_required()
def add_team_member():
    data = request.get_json()
    member = TeamMember(
        id=data['id'],
        name=data['name'],
        email=data['email'],
        phone_number=data['phone_number'],
        role=data['role']
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Team member added successfully'}), 201

@team_member_bp.route('/team/<id>', methods=['PUT'])
@jwt_required()
def update_team_member(id):
    member = TeamMember.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(member, key, value)
    db.session.commit()
    return jsonify({'message': 'Team member updated successfully'}), 200

@team_member_bp.route('/team/<id>', methods=['DELETE'])
@jwt_required()
def delete_team_member(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Team member deleted successfully'}), 200