class Config:
    SECRET_KEY = 'your-secret-key-here'  # Replace with generated secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///health_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-jwt-secret-key-here'  # Replace with another generated secret key