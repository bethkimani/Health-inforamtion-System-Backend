from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from models.client import Client
from models.appointment import Appointment
from models.program import Program
from app import db
from sqlalchemy import func, extract
from datetime import datetime, timedelta

dashboard_ns = Namespace('dashboard', description='Dashboard metrics')

@dashboard_ns.route('/metrics')
class DashboardMetrics(Resource):
    @jwt_required()
    def get(self):
        # Total patients
        total_patients = Client.query.count()

        # Patients per month (for histogram)
        patients_per_month = db.session.query(
            extract('month', Client.created_at).label('month'),
            func.count(Client.id).label('count')
        ).group_by(extract('month', Client.created_at)).all()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        patients_data = [0] * 12
        for month, count in patients_per_month:
            patients_data[int(month) - 1] = count

        # Appointment status counts (for pie chart)
        appointment_status = db.session.query(
            Appointment.status,
            func.count(Appointment.id).label('count')
        ).group_by(Appointment.status).all()
        status_counts = {'Approved': 0, 'Pending': 0, 'Rejected': 0}
        for status, count in appointment_status:
            status_counts[status] = count

        # Recent appointments (queue)
        recent_appointments = Appointment.query.join(Client).join(Program).order_by(
            Appointment.requested_at.desc()
        ).limit(5).all()

        return {
            'total_patients': total_patients,
            'triage': Client.query.filter_by(status='triage').count(),  # Example filter
            'lab': Client.query.filter_by(status='lab').count(),  # Example filter
            'pharmacy': Client.query.filter_by(status='pharmacy').count(),  # Example filter
            'patients_per_month': {
                'labels': months,
                'data': patients_data
            },
            'appointment_status': status_counts,
            'recent_appointments': [{
                'id': a.id,
                'visit_no': f"A{a.id:06d}",
                'client_name': f"{a.client.first_name} {a.client.last_name}",
                'check_in_date': a.requested_at.strftime('%Y-%m-%d'),
                'status': a.status
            } for a in recent_appointments]
        }, 200