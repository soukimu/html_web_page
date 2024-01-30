from datetime import datetime
from .db import db


class HasSent(db.Model):
    __tablename__ = 'has_sent'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    