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
    'phone': fields.String,
    'dob': fields.String,
    'gender': fields.String,
    'status': fields.String
})

@client_ns.route('')
class ClientList(Resource):
    @jwt_required()
    @client_ns.marshal_list_with(client_model)
    def get(self):
        return Client.query.all()

    @jwt_required()
    @client_ns.expect(client_model, validate=True)
    @client_ns.marshal_with(client_model, code=201)
    def post(self):
        data = client_ns.payload
        if Client.query.filter_by(email=data['email']).first():
            client_ns.abort(400, message='Email already exists')
        client = Client(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            status=data.get('status', 'active')
        )
        db.session.add(client)
        db.session.commit()
        return client, 201

@client_ns.route('/<int:id>')
class ClientDetail(Resource):
    @jwt_required()
    @client_ns.marshal_with(client_model)
    def get(self, id):
        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message='Client not found')
        return client

    @jwt_required()
    @client_ns.expect(client_model, validate=True)
    @client_ns.marshal_with(client_model)
    def put(self, id):
        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message='Client not found')
        data = client_ns.payload
        if Client.query.filter_by(email=data['email']).filter(Client.id != id).first():
            client_ns.abort(400, message='Email already exists')
        for key in ['first_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'status']:
            if key in data:
                setattr(client, key, data[key])
        db.session.commit()
        return client

    @jwt_required()
    def delete(self, id):
        client = Client.query.get(id)
        if not client:
            client_ns.abort(404, message='Client not found')
        db.session.delete(client)
        db.session.commit()
        return {'message': 'Client deleted'}, 200