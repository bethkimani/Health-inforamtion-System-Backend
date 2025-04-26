from models import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    file_url = db.Column(db.String(200), nullable=False)