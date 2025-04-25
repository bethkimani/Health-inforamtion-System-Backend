import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "health_system.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', '6195a52892f58c880a90916f0c5f6102')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '9ae9a72f2ca05a7b1b798e30306a634')
    