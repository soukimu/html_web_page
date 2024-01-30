from datetime import datetime
from .db import db


class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable=False)  # 'M' for male, 'F' for female
    has_pair = db.Column(db.Boolean, default=False, nullable=False)

class Pairing(db.Model):
    __tablename__ = 'pairings'
    
    id = db.Column(db.Integer, primary_key=True)
    giver_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    taker_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    
    giver = db.relationship('Participant', foreign_keys=[giver_id])
    taker = db.relationship('Participant', foreign_keys=[taker_id])