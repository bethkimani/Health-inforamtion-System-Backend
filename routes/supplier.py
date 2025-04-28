from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.supplier import Supplier
from models.document import Document
from models import db
from datetime import datetime

supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/suppliers', methods=['GET'])
#@jwt_required()
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'email': s.email,
        'phone': s.phone,
        'status': s.status,
        'bio': s.bio,
        'license_number': s.license_number,
        'address': s.address,
        'city': s.city,
        'country': s.country,
        'county': s.county,
        'postal_code': s.postal_code,
        'contact_person_name': s.contact_person_name,
        'contact_person_email': s.contact_person_email,
        'contact_person_phone': s.contact_person_phone,
        'contract_start_date': s.contract_start_date.isoformat() if s.contract_start_date else None,
        'contract_end_date': s.contract_end_date.isoformat() if s.contract_end_date else None,
        'supply_category': s.supply_category,
        'certifications': s.certifications,
        'delivery_frequency': s.delivery_frequency,
        'next_delivery_date': s.next_delivery_date.isoformat() if s.next_delivery_date else None,
        'delivery_notes': s.delivery_notes,
        'documents': [{'filename': d.filename, 'type': d.type, 'file_url': d.file_url} for d in s.documents]
    } for s in suppliers]), 200

@supplier_bp.route('/suppliers', methods=['POST'])
#@jwt_required()
def add_supplier():
    data = request.get_json()
    supplier = Supplier(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        bio=data.get('bio'),
        license_number=data.get('license_number'),
        address=data.get('address'),
        city=data.get('city'),
        country=data.get('country'),
        county=data.get('county'),
        postal_code=data.get('postal_code'),
        contact_person_name=data.get('contact_person_name'),
        contact_person_email=data.get('contact_person_email'),
        contact_person_phone=data.get('contact_person_phone'),
        status=data.get('status', True),
        contract_start_date=datetime.strptime(data['contract_start_date'], '%Y-%m-%d') if data.get('contract_start_date') else None,
        contract_end_date=datetime.strptime(data['contract_end_date'], '%Y-%m-%d') if data.get('contract_end_date') else None,
        supply_category=data.get('supply_category'),
        certifications=data.get('certifications'),
        delivery_frequency=data.get('delivery_frequency'),
        next_delivery_date=datetime.strptime(data['next_delivery_date'], '%Y-%m-%d') if data.get('next_delivery_date') else None,
        delivery_notes=data.get('delivery_notes')
    )
    db.session.add(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier added successfully'}), 201

@supplier_bp.route('/suppliers/<int:id>', methods=['PUT'])
#@jwt_required()
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        if key in ['contract_start_date', 'contract_end_date', 'next_delivery_date'] and value:
            value = datetime.strptime(value, '%Y-%m-%d')
        setattr(supplier, key, value)
    db.session.commit()
    return jsonify({'message': 'Supplier updated successfully'}), 200

@supplier_bp.route('/suppliers/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted successfully'}), 200

@supplier_bp.route('/suppliers/<int:id>/documents', methods=['POST'])
#@jwt_required()
def upload_document(id):
    supplier = Supplier.query.get_or_404(id)
    data = request.form
    file = request.files.get('file')
    if not file:
        return jsonify({'message': 'No file uploaded'}), 400
    filename = file.filename
    file_url = f"/uploads/{filename}"  # Simulate file storage
    document = Document(
        supplier_id=supplier.id,
        filename=data['documentName'],
        type=data['documentType'],
        file_url=file_url
    )
    db.session.add(document)
    db.session.commit()
    return jsonify({'message': 'Document uploaded successfully'}), 201