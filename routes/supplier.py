from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db
from models.supplier import Supplier

supplier_ns = Namespace('suppliers', description='Supplier operations')

supplier_model = supplier_ns.model('Supplier', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'contact_info': fields.String(required=False),
    'contract_details': fields.String(required=False)
})

@supplier_ns.route('')
class SupplierList(Resource):
    @jwt_required()
    @supplier_ns.marshal_list_with(supplier_model)
    def get(self):
        return Supplier.query.all(), 200

    @jwt_required()
    @supplier_ns.expect(supplier_model, validate=False)
    @supplier_ns.marshal_with(supplier_model, code=201)
    def post(self):
        data = supplier_ns.payload
        if not data.get('name'):
            return {'message': 'name is required and cannot be empty'}, 400
        supplier = Supplier(
            name=data['name'],
            contact_info=data.get('contact_info'),
            contract_details=data.get('contract_details')
        )
        db.session.add(supplier)
        db.session.commit()
        return supplier, 201