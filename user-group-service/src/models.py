from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.String(128), nullable=False)  # Changed to String for Firebase UID
    members = db.relationship('GroupMember', backref='group', lazy=True)
    secret_questions = db.relationship('SecretQuestion', backref='group', lazy=True)

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)  # Changed to String for Firebase UID
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    role = db.Column(db.String(20), default='member')
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

class SecretQuestion(db.Model):
    __tablename__ = 'secret_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    created_by = db.Column(db.String(128), nullable=False)  # Changed to String for Firebase UID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)