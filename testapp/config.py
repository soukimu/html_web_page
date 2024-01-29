import os

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

DATABASE_URL = os.environ.get('DATABASE_URL') or "postgresql://localhost/flasknote"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = DATABASE_URL
