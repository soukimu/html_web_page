import os
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://localhost/flasknote"
SQLALCHEMY_TRACK_MODIFICATIONS = True