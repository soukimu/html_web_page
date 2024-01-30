from datetime import datetime
from .db import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(50))
    gender = db.Column(db.String(1), nullable=False)  # 'M' for male, 'F' for female
    has_pair = db.Column(db.Boolean, default=False, nullable=False)
    like = db.Column(db.String(255))
