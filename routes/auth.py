from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app import db
from models.user import User

auth_ns = Namespace('auth', description='Authentication operations')

register_model = auth_ns.model('Register', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=True)
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        data = auth_ns.payload
        if User.query.filter_by(email=data['email']).first():
            auth_ns.abort(400, message='Email already exists')
        user = User(email=data['email'], role=data['role'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        data = auth_ns.payload
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            auth_ns.abort(401, message='Invalid credentials')
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200