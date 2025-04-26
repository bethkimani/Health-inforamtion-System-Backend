from models import db

class HealthRecord(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    client_id = db.Column(db.String(10), db.ForeignKey('client.id'), nullable=False)
    program_id = db.Column(db.String(10), db.ForeignKey('program.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Active')
    notes = db.Column(db.Text)