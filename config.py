import os

class Config:
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:qqqq@localhost:5432/catalog_db"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.getenv("SECRET_KEY", "secret_landsknecht")