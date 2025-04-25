from app import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    dob = db.Column(db.String(10))
    gender = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')  # Added for dashboard metrics
    enrollments = db.relationship('Enrollment', backref='client', lazy=True)
    appointments = db.relationship('Appointment', backref='client', lazy=True)