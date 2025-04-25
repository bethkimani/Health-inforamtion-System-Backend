from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models.program import Program
from app import db

program_ns = Namespace('programs', description='Program operations')

program_model = program_ns.model('Program', {
    'name': fields.String(required=True),
    'description': fields.String
})

@program_ns.route('')
class ProgramList(Resource):
    @jwt_required()
    @program_ns.expect(program_model)
    def post(self):
        data = program_ns.payload
        if Program.query.filter_by(name=data['name']).first():
            return {'message': 'Program already exists'}, 400
        program = Program(**data)
        db.session.add(program)
        db.session.commit()
        return {'message': 'Program created successfully', 'program_id': program.id}, 201

    @jwt_required()
    def get(self):
        programs = Program.query.all()
        return [{
            'id': p.id,
            'name': p.name,
            'description': p.description
        } for p in programs], 200