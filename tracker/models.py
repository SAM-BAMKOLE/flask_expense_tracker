from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy import Enum
import enum

class User(db.Model, UserMixin):
    id                  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email           = db.Column(db.String(255), unique=True, nullable=False)
    password_hash   = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    transanctions = db.relationship('Transanction')

class TransanctionType(str, enum.Enum):
    income = 'income'
    expense = 'expense'

class Transanction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    # TODO: currency = db.Column
    type = db.Column(Enum(TransanctionType), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    date  = db.Column(db.DateTime, default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_type()
    
    def validate_type(self):
        if self.type not in ['income', 'expense']:
            raise ValueError('Invalid transanction type, must be \'income\' or \'expense\'.')

