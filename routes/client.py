from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.client import Client

client_ns = Namespace('clients', description='Client operations')

client_model = client_ns.model('Client', {
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
    @client_ns.expect(client_model)
    @client_ns.marshal_with(client_model, code=201)
    def post(self):
        data = client_ns.payload
        client = Client(**data)
        db.session.add(client)
        db.session.commit()
        return client, 201

@client_ns.route('/<int:id>')
class ClientDetail(Resource):
    @jwt_required()
    @client_ns.marshal_with(client_model)
    def get(self, id):
        client = Client.query.get_or_404(id)
        return client

    @jwt_required()
    @client_ns.expect(client_model)
    @client_ns.marshal_with(client_model)
    def put(self, id):
        client = Client.query.get_or_404(id)
        data = client_ns.payload
        for key, value in data.items():
            setattr(client, key, value)
        db.session.commit()
        return client

    @jwt_required()
    def delete(self, id):
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return {'message': 'Client deleted'}, 200