from models import db

class ClientProgram(db.Model):
    client_id = db.Column(db.String(10), db.ForeignKey('client.id'), primary_key=True)
    program_id = db.Column(db.String(10), db.ForeignKey('program.id'), primary_key=True)