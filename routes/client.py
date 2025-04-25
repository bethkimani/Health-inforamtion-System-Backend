from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models.client import Client
from models.enrollment import Enrollment
from models.program import Program
from app import db

client_ns = Namespace('clients', description='Client operations')

client_model = client_ns.model('Client', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'phone': fields.String,
    'dob': fields.String,
    'gender': fields.String
})

enrollment_model = client_ns.model('Enrollment', {
    'client_id': fields.Integer(required=True),
    'program_id': fields.Integer(required=True)
})

@client_ns.route('')
class ClientList(Resource):
    @jwt_required()
    @client_ns.expect(client_model)
    def post(self):
        data = client_ns.payload
        if Client.query.filter_by(email=data['email']).first():
            return {'message': 'Client already exists'}, 400
        client = Client(**data)
        db.session.add(client)
        db.session.commit()
        return {'message': 'Client registered successfully', 'client_id': client.id}, 201

    @jwt_required()
    def get(self):
        parser = client_ns.parser()
        parser.add_argument('search', type=str)
        args = parser.parse_args()
        query = Client.query
        if args['search']:
            search = f"%{args['search']}%"
            query = query.filter(
                (Client.first_name.ilike(search)) |
                (Client.last_name.ilike(search)) |
                (Client.email.ilike(search))
            )
        clients = query.all()
        return [{
            'id': c.id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email': c.email,
            'phone': c.phone,
            'dob': c.dob,
            'gender': c.gender,
            'programs': [e.program.name for e in c.enrollments]
        } for c in clients], 200

@client_ns.route('/<int:id>')
class ClientDetail(Resource):
    @jwt_required()
    def get(self, id):
        client = Client.query.get_or_404(id)
        enrollments = Enrollment.query.filter_by(client_id=id).all()
        programs = [{
            'id': e.program.id,
            'name': e.program.name,
            'enrollment_date': e.enrollment_date.isoformat()
        } for e in enrollments]
        return {
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'phone': client.phone,
            'dob': client.dob,
            'gender': client.gender,
            'programs': programs
        }, 200

@client_ns.route('/enroll')
class ClientEnrollment(Resource):
    @jwt_required()
    @client_ns.expect(enrollment_model)
    def post(self):
        data = client_ns.payload
        if not Client.query.get(data['client_id']) or not Program.query.get(data['program_id']):
            return {'message': 'Client or Program not found'}, 404
        if Enrollment.query.filter_by(client_id=data['client_id'], program_id=data['program_id']).first():
            return {'message': 'Client already enrolled in this program'}, 400
        enrollment = Enrollment(client_id=data['client_id'], program_id=data['program_id'])
        db.session.add(enrollment)
        db.session.commit()
        return {'message': 'Client enrolled successfully'}, 201