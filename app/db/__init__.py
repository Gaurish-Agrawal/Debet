from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    age = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    tokens = db.Column(db.Integer, default = 20) #1 token = 0.5 dollars

    def __init__(self, name, email, password, age, gender):
        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender


class Debate(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    attacker = db.Column(db.String(100))
    defendent = db.Column(db.String(100))
    description = db.Column(db.String(300))
    timestamp = db.Column(db.String(300))
    closed = db.Column(db.Boolean, default=False, nullable=False)
    ongoing = db.Column(db.Boolean, default=False, nullable=False)
    attacker_amount = db.Column(db.Integer, nullable = False)
    defender_amount = db.Column(db.Integer, nullable = False)
    created_by = db.Column(db.Integer)
    total_amount = db.Column(db.Integer, nullable = False)

    def __init__(self, name, attacker, defendent, description, closed, ongoing, attacker_amount, defender_amount, created_by, responded_by, total_amount, timestamp):
        self.name = name
        self.attacker = attacker
        self.defendent = defendent
        self.description = description
        self.closed = closed
        self.ongoing = ongoing
        self.attacker_amount = attacker_amount
        self.defender_amount = defender_amount
        self.created_by = created_by
        self.total_amount = total_amount
        self.timestamp = timestamp




class Message(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    debate_id = db.Column(db.Integer, nullable = False)
    text = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=pytz.timezone('US/Pacific')))
    created_by = db.Column(db.Integer)

    def __init__(self, text, timestamp, created_by):
        self.text = db.Column(db.String(300))
        self.created_by = created_by
