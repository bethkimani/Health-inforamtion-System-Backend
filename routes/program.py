from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.program import Program

program_ns = Namespace('programs', description='Program operations')

program_model = program_ns.model('Program', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(required=False)
})

@program_ns.route('')
class ProgramList(Resource):
    @jwt_required()
    @program_ns.marshal_list_with(program_model)
    def get(self):
        return Program.query.all(), 200

    @jwt_required()
    @program_ns.expect(program_model, validate=False)
    @program_ns.marshal_with(program_model, code=201)
    def post(self):
        data = program_ns.payload
        program = Program(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(program)
        db.session.commit()
        return program, 201