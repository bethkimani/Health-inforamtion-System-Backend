
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.appointment import Appointment
from models.client import Client
from models.program import Program

appointment_ns = Namespace('appointments', description='Appointment operations')

appointment_model = appointment_ns.model('Appointment', {
    'id': fields.Integer(readonly=True),
    'client_id': fields.Integer(required=True),
    'program_id': fields.Integer(required=True),
    'status': fields.String(required=True),
    'requested_at': fields.DateTime(readonly=True)
})

@appointment_ns.route('')
class AppointmentList(Resource):
    @jwt_required()
    @appointment_ns.marshal_list_with(appointment_model)
    def get(self):
        return Appointment.query.all()

    @jwt_required()
    @appointment_ns.expect(appointment_model, validate=True)
    @appointment_ns.marshal_with(appointment_model, code=201)
    def post(self):
        data = appointment_ns.payload
        if not Client.query.get(data['client_id']):
            appointment_ns.abort(400, message='Invalid client_id')
        if not Program.query.get(data['program_id']):
            appointment_ns.abort(400, message='Invalid program_id')
        appointment = Appointment(
            client_id=data['client_id'],
            program_id=data['program_id'],
            status=data['status']
        )
        db.session.add(appointment)
        db.session.commit()
        return appointment, 201