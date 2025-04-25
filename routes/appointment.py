from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.appointment import Appointment

appointment_ns = Namespace('appointments', description='Appointment operations')

appointment_model = appointment_ns.model('Appointment', {
    'client_id': fields.Integer(required=True),
    'program_id': fields.Integer(required=True),
    'status': fields.String(required=True)
})

@appointment_ns.route('')
class AppointmentList(Resource):
    @jwt_required()
    @appointment_ns.marshal_list_with(appointment_model)
    def get(self):
        return Appointment.query.all()

    @jwt_required()
    @appointment_ns.expect(appointment_model)
    @appointment_ns.marshal_with(appointment_model, code=201)
    def post(self):
        data = appointment_ns.payload
        appointment = Appointment(**data)
        db.session.add(appointment)
        db.session.commit()
        return appointment, 201