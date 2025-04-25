import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '6195a52892f58c880a90916f0c5f6102')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///instance/health_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '9ae9a72f2ca05a7b1b798e30306a634')