from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.client import Client

client_ns = Namespace('clients', description='Client operations')

client_model = client_ns.model('Client', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'phone': fields.String(required=False),
    'dob': fields.String(required=False),
    'gender': fields.String(required=False),
    'status': fields.String(required=True)
})

@client_ns.route('')
class ClientList(Resource):
    @jwt_required()
    @client_ns.marshal_list_with(client_model)
    def get(self):
        return Client.query.all(), 200

    @jwt_required()
    @client_ns.expect(client_model, validate=False)
    @client_ns.marshal_with(client_model, code=201)
    def post(self):
        data = client_ns.payload
        if Client.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400
        client = Client(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            status=data['status']
        )
        db.session.add(client)
        db.session.commit()
        return client, 201

@client_ns.route('/<int:id>')
class ClientResource(Resource):
    @jwt_required()
    @client_ns.marshal_with(client_model)
    def get(self, id):
        client = Client.query.get_or_404(id)
        return client, 200

    @jwt_required()
    @client_ns.expect(client_model, validate=False)
    @client_ns.marshal_with(client_model)
    def put(self, id):
        client = Client.query.get_or_404(id)
        data = client_ns.payload
        if 'email' in data and data['email'] != client.email:
            if Client.query.filter_by(email=data['email']).first():
                return {'message': 'Email already exists'}, 400
        client.first_name = data['first_name']
        client.last_name = data['last_name']
        client.email = data['email']
        client.phone = data.get('phone')
        client.dob = data.get('dob')
        client.gender = data.get('gender')
        client.status = data['status']
        db.session.commit()
        return client, 200

    @jwt_required()
    def delete(self, id):
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return {'message': 'Client deleted'}, 200