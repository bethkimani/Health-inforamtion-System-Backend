from app import db
from datetime import datetime, timezone

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    requested_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))