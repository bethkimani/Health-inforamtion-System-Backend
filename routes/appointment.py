from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models.appointment import Appointment
from models.client import Client
from models.program import Program
from app import db
from datetime import datetime

appointment_ns = Namespace('appointments', description='Appointment operations')

appointment_model = appointment_ns.model('Appointment', {
    'client_id': fields.Integer(required=True),
    'program_id': fields.Integer(required=True),
    'requested_at': fields.DateTime
})

update_status_model = appointment_ns.model('UpdateStatus', {
    'status': fields.String(required=True, enum=['Pending', 'Approved', 'Rejected'])
})

@appointment_ns.route('')
class AppointmentList(Resource):
    @jwt_required()
    @appointment_ns.expect(appointment_model)
    def post(self):
        data = appointment_ns.payload
        if not Client.query.get(data['client_id']) or not Program.query.get(data['program_id']):
            return {'message': 'Client or Program not found'}, 404
        appointment = Appointment(
            client_id=data['client_id'],
            program_id=data['program_id'],
            requested_at=data.get('requested_at', datetime.utcnow())
        )
        db.session.add(appointment)
        db.session.commit()
        return {'message': 'Appointment created successfully', 'appointment_id': appointment.id}, 201

    @jwt_required()
    def get(self):
        parser = appointment_ns.parser()
        parser.add_argument('search', type=str)
        parser.add_argument('program', type=str, action='append')
        parser.add_argument('status', type=str, action='append')
        args = parser.parse_args()
        
        query = Appointment.query.join(Client).join(Program)
        if args['search']:
            search = f"%{args['search']}%"
            query = query.filter(
                (Client.first_name.ilike(search)) |
                (Client.last_name.ilike(search)) |
                (Program.name.ilike(search))
            )
        if args['program']:
            query = query.filter(Program.name.in_(args['program']))
        if args['status']:
            query = query.filter(Appointment.status.in_(args['status']))
        
        appointments = query.all()
        return [{
            'id': a.id,
            'client_id': a.client_id,
            'client_name': f"{a.client.first_name} {a.client.last_name}",
            'program': a.program.name,
            'requested_at': a.requested_at.isoformat(),
            'status': a.status
        } for a in appointments], 200

@appointment_ns.route('/<int:id>/status')
class AppointmentStatus(Resource):
    @jwt_required()
    @appointment_ns.expect(update_status_model)
    def put(self, id):
        data = appointment_ns.payload
        appointment = Appointment.query.get_or_404(id)
        appointment.status = data['status']
        db.session.commit()
        return {'message': f'Appointment status updated to {data["status"]}'}, 200