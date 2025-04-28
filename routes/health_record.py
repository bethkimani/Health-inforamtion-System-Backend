from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.health_record import HealthRecord
from models import db

health_record_bp = Blueprint('health_record', __name__)

@health_record_bp.route('/health-records', methods=['GET'])
#@jwt_required()
def get_health_records():
    records = HealthRecord.query.all()
    return jsonify([{
        'id': r.id,
        'client_id': r.client_id,
        'client_name': f"{r.client.first_name} {r.client.last_name}",
        'program': r.program.name,
        'date': r.date.isoformat(),
        'status': r.status,
        'notes': r.notes
    } for r in records]), 200

@health_record_bp.route('/health-records/<id>/complete', methods=['PATCH'])
#@jwt_required()
def complete_health_record(id):
    record = HealthRecord.query.get_or_404(id)
    record.status = 'Completed'
    db.session.commit()
    return jsonify({'message': 'Health record marked as completed'}), 200