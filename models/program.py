from app import db

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    enrollments = db.relationship('Enrollment', backref='program', lazy=True)
    appointments = db.relationship('Appointment', backref='program', lazy=True)