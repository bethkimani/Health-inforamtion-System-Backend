from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .appointment import Appointment
from .client import Client
from .client_program import ClientProgram
from .document import Document
from .health_record import HealthRecord
from .program import Program
from .supplier import Supplier
from .team_member import TeamMember
from .user import User