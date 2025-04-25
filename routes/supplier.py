from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models.supplier import Supplier
from app import db
from datetime import datetime

supplier_ns = Namespace('suppliers', description='Supplier operations')

supplier_model = supplier_ns.model('Supplier', {
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'phone': fields.String,
    'bio': fields.String,
    'license_number': fields.String,
    'address': fields.String,
    'city': fields.String,
    'county': fields.String,
    'country': fields.String,
    'postal_code': fields.String,
    'contact_person_name': fields.String,
    'contact_person_email': fields.String,
    'contact_person_phone': fields.String,
    'status': fields.Boolean,
    'contract_start_date': fields.Date,
    'contract_end_date': fields.Date,
    'supply_category': fields.String,
    'certifications': fields.String,
    'delivery_frequency': fields.String,
    'next_delivery_date': fields.Date,
    'delivery_notes': fields.String
})

@supplier_ns.route('')
class SupplierList(Resource):
    @jwt_required()
    @supplier_ns.expect(supplier_model)
    def post(self):
        data = supplier_ns.payload
        if Supplier.query.filter_by(email=data['email']).first():
            return {'message': 'Supplier already exists'}, 400
        supplier = Supplier(**data)
        db.session.add(supplier)
        db.session.commit()
        return {'message': 'Supplier created successfully', 'supplier_id': supplier.id}, 201

    @jwt_required()
    def get(self):
        parser = supplier_ns.parser()
        parser.add_argument('search', type=str)
        parser.add_argument('status', type=str)
        args = parser.parse_args()
        
        query = Supplier.query
        if args['search']:
            search = f"%{args['search']}%"
            query = query.filter(Supplier.name.ilike(search))
        if args['status']:
            query = query.filter(Supplier.status == (args['status'] == 'true'))
        
        suppliers = query.all()
        return [{
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'phone': s.phone,
            'status': s.status
        } for s in suppliers], 200

@supplier_ns.route('/<int:id>')
class SupplierDetail(Resource):
    @jwt_required()
    def get(self, id):
        supplier = Supplier.query.get_or_404(id)
        return {
            'id': supplier.id,
            'name': supplier.name,
            'email': supplier.email,
            'phone': supplier.phone,
            'bio': supplier.bio,
            'license_number': supplier.license_number,
            'address': supplier.address,
            'city': supplier.city,
            'county': supplier.county,
            'country': supplier.country,
            'postal_code': supplier.postal_code,
            'contact_person_name': supplier.contact_person_name,
            'contact_person_email': supplier.contact_person_email,
            'contact_person_phone': supplier.contact_person_phone,
            'status': supplier.status,
            'contract_start_date': supplier.contract_start_date.isoformat() if supplier.contract_start_date else None,
            'contract_end_date': supplier.contract_end_date.isoformat() if supplier.contract_end_date else None,
            'supply_category': supplier.supply_category,
            'certifications': supplier.certifications,
            'delivery_frequency': supplier.delivery_frequency,
            'next_delivery_date': supplier.next_delivery_date.isoformat() if supplier.next_delivery_date else None,
            'delivery_notes': supplier.delivery_notes
        }, 200

    @jwt_required()
    @supplier_ns.expect(supplier_model)
    def put(self, id):
        supplier = Supplier.query.get_or_404(id)
        data = supplier_ns.payload
        for key, value in data.items():
            setattr(supplier, key, value)
        db.session.commit()
        return {'message': 'Supplier updated successfully'}, 200

    @jwt_required()
    def delete(self, id):
        supplier = Supplier.query.get_or_404(id)
        db.session.delete(supplier)
        db.session.commit()
        return {'message': 'Supplier deleted successfully'}, 200

@supplier_ns.route('/<int:id>/status')
class SupplierStatus(Resource):
    @jwt_required()
    def put(self, id):
        supplier = Supplier.query.get_or_404(id)
        supplier.status = not supplier.status
        db.session.commit()
        return {'message': f'Supplier status updated to {"Active" if supplier.status else "Inactive"}'}, 200