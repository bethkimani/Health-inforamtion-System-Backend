from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.client import Client
from models.program import Program
from models.appointment import Appointment

dashboard_ns = Namespace('dashboard', description='Dashboard operations')

metrics_model = dashboard_ns.model('Metrics', {
    'total_clients': fields.Integer(),
    'total_programs': fields.Integer(),
    'total_appointments': fields.Integer()
})

@dashboard_ns.route('/metrics')
class DashboardMetrics(Resource):
    @jwt_required()
    @dashboard_ns.marshal_with(metrics_model)
    def get(self):
        metrics = {
            'total_clients': Client.query.count(),
            'total_programs': Program.query.count(),
            'total_appointments': Appointment.query.count()
        }
        return metrics, 200