from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app import db
from models.client import Client
from models.appointment import Appointment
from models.program import Program

dashboard_ns = Namespace('dashboard', description='Dashboard operations')

@dashboard_ns.route('/metrics')
class DashboardMetrics(Resource):
    @jwt_required()
    def get(self):
        total_patients = Client.query.count()
        appointment_status = {
            'Pending': Appointment.query.filter_by(status='Pending').count(),
            'Approved': Appointment.query.filter_by(status='Approved').count(),
            'Completed': Appointment.query.filter_by(status='Completed').count()
        }
        recent_appointments = [
            {
                'id': appt.id,
                'client_name': f"{appt.client.first_name} {appt.client.last_name}",
                'program_name': appt.program.name,
                'status': appt.status,
                'requested_at': appt.requested_at.isoformat()
            }
            for appt in Appointment.query.order_by(Appointment.requested_at.desc()).limit(5).all()
        ]
        status_counts = {
            'triage': Client.query.filter_by(status='triage').count(),
            'lab': Client.query.filter_by(status='lab').count(),
            'pharmacy': Client.query.filter_by(status='pharmacy').count()
        }
        return {
            'total_patients': total_patients,
            'appointment_status': appointment_status,
            'recent_appointments': recent_appointments,
            'status_counts': status_counts
        }, 200