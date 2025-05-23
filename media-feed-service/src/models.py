from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    """
    Model class for posts in the media feed service.
    Inherits from SQLAlchemy's Model class.
    """
    __bind_key__ = None  # This tells Flask-SQLAlchemy to use the default database
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)  # Changed to String for Firebase UID
    group_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)  # Changed from image_path
    caption = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'image_url': self.image_url,  # Changed from image_path
            'caption': self.caption,
            'created_at': self.created_at.isoformat()
        }

class DailyChallenge(db.Model):  # type: ignore
    """
    Model class for daily challenges in the media feed service.
    Inherits from SQLAlchemy's Model class.
    """
    __bind_key__ = None  # This tells Flask-SQLAlchemy to use the default database
    __tablename__ = 'daily_challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False)
    challenge_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    completed_users = db.Column(db.JSON, default=list)  # Changed to JSON type for flexibility
