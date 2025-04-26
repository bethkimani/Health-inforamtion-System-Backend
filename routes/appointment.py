from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.appointment import Appointment
from models import db

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'id': a.id,
        'client_id': a.client_id,
        'client_name': f"{a.client.first_name} {a.client.last_name}",
        'program': a.program.name,
        'requested_at': a.requested_at.isoformat(),
        'status': a.status
    } for a in appointments]), 200

@appointment_bp.route('/appointments/<id>/approve', methods=['PATCH'])
@jwt_required()
def approve_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'Approved'
    db.session.commit()
    return jsonify({'message': 'Appointment approved'}), 200

@appointment_bp.route('/appointments/<id>/reject', methods=['PATCH'])
@jwt_required()
def reject_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'Rejected'
    db.session.commit()
    return jsonify({'message': 'Appointment rejected'}), 200