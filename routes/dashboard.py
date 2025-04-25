from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.client import Client
from models.appointment import Appointment

dashboard_ns = Namespace('dashboard', description='Dashboard operations')

dashboard_model = dashboard_ns.model('Dashboard', {
    'total_patients': fields.Integer,
    'appointment_status': fields.Nested(dashboard_ns.model('AppointmentStatus', {
        'Pending': fields.Integer,
        'Approved': fields.Integer,
        'Completed': fields.Integer
    })),
    'recent_appointments': fields.List(fields.Nested(dashboard_ns.model('RecentAppointment', {
        'id': fields.Integer,
        'client_id': fields.Integer,
        'status': fields.String
    }))),
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
        return {
            'total_patients': Client.query.count(),
            'appointment_status': {
                'Pending': Appointment.query.filter_by(status='Pending').count(),
                'Approved': Appointment.query.filter_by(status='Approved').count(),
                'Completed': Appointment.query.filter_by(status='Completed').count()
            },
            'recent_appointments': Appointment.query.order_by(Appointment.requested_at.desc()).limit(5).all(),
            'status_counts': {
                'triage': Client.query.filter_by(status='triage').count(),
                'lab': Client.query.filter_by(status='lab').count(),
                'pharmacy': Client.query.filter_by(status='pharmacy').count()
            }
        }