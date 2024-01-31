from datetime import datetime
from .db import db


class Pairing(db.Model):
    __tablename__ = 'pairings'
    
    id = db.Column(db.Integer, primary_key=True)
    giver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    giver = db.relationship('User', foreign_keys=[giver_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
