from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.client import Client
from models.appointment import Appointment

dashboard_ns = Namespace('dashboard', description='Dashboard operations')

appointment_model = dashboard_ns.model('RecentAppointment', {
    'id': fields.Integer,
    'client_id': fields.Integer,
    'status': fields.String,
    'client_name': fields.String,
    'program_id': fields.Integer,
    'requested_at': fields.DateTime
})

dashboard_model = dashboard_ns.model('Dashboard', {
    'total_patients': fields.Integer,
    'appointment_status': fields.Nested(dashboard_ns.model('AppointmentStatus', {
        'Pending': fields.Integer,
        'Approved': fields.Integer,
        'Completed': fields.Integer
    })),
    'recent_appointments': fields.List(fields.Nested(appointment_model)),
    'status_counts': fields.Nested(dashboard_ns.model('StatusCounts', {
        'triage': fields.Integer,
        'lab': fields.Integer,
        'pharmacy': fields.Integer
    }))
})

@dashboard_ns.route('/metrics')
class DashboardMetrics(Resource):
    @jwt_required()
    @dashboard_ns.marshal_with(dashboard_model)
    def get(self):
        recent_appointments = Appointment.query.order_by(Appointment.requested_at.desc()).limit(5).all()
        recent_appointments_data = []
        for appt in recent_appointments:
            client = Client.query.get(appt.client_id)
            appt_data = {
                'id': appt.id,
                'client_id': appt.client_id,
                'status': appt.status,
                'client_name': f"{client.first_name} {client.last_name}" if client else "Unknown",
                'program_id': appt.program_id,
                'requested_at': appt.requested_at
            }
            recent_appointments_data.append(appt_data)
        return {
            'total_patients': Client.query.count(),
            'appointment_status': {
                'Pending': Appointment.query.filter_by(status='Pending').count(),
                'Approved': Appointment.query.filter_by(status='Approved').count(),
                'Completed': Appointment.query.filter_by(status='Completed').count()
            },
            'recent_appointments': recent_appointments_data,
            'status_counts': {
                'triage': Client.query.filter_by(status='triage').count(),
                'lab': Client.query.filter_by(status='lab').count(),
                'pharmacy': Client.query.filter_by(status='pharmacy').count()
            }
        }