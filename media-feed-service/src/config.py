import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv(override=True)

JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))

class Config:
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5002))

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/media_feed_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=JWT_EXPIRATION_HOURS)

    # Services URLs
    USER_GROUP_SERVICE_URL = os.getenv('USER_GROUP_SERVICE_URL', 'http://localhost:5002')
    
    print(f'DB: {SQLALCHEMY_DATABASE_URI}')
