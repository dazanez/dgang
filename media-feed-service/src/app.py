import os
from datetime import datetime, date
from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Post, DailyChallenge, db
import jwt
from functools import wraps
import requests
from config import Config

migrate = Migrate()

def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    
    return flask_app

app = create_app()

# Initialize database
with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            # Explicitly use the secret key from config
            secret_key = app.config['JWT_SECRET_KEY']
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            if 'uid' not in data:  # Changed from 'user_id' to 'uid'
                return jsonify({'message': 'Invalid token format'}), 401
            current_user = data['uid']  # Changed from 'user_id' to 'uid'
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated



def verify_group_membership(user_id, group_id):
    # Get the token from the current request
    token = request.headers.get('Authorization')
    if not token:
        return False

    # Call User Group Service to verify membership with the Authorization header
    headers = {
        'Authorization': token  # Forward the original token
    }
    
    response = requests.get(
        f"{app.config['USER_GROUP_SERVICE_URL']}/api/v1/groups/{group_id}/members",
        headers=headers
    )

    if response.status_code != 200:
        return False
        
    members = response.json()
    
    # Check if user exists in members list and has active status
    return any(
        member['user_id'] == user_id and 
        member['status'] == 'active' 
        for member in members
    )

@app.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()
    
    if not data or 'image_url' not in data or 'group_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    image_url = data['image_url']
    group_id = data['group_id']
    caption = data.get('caption', '')
    
    if not verify_group_membership(current_user, group_id):
        return jsonify({'error': 'User is not a member of this group'}), 403
    
    # Create post with URL
    post = Post(
        user_id=current_user,
        group_id=group_id,
        image_url=image_url,
        caption=caption
    )
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@app.route('/groups/<int:group_id>/feed', methods=['GET'])
@token_required
def get_group_feed(current_user, group_id):
    if not verify_group_membership(current_user, group_id):
        return jsonify({'error': 'User is not a member of this group'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.filter_by(group_id=group_id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    })

@app.route('/posts/<int:post_id>/image', methods=['GET'])
@token_required
def get_post_image(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    if not verify_group_membership(current_user, post.group_id):
        return jsonify({'error': 'User is not a member of this group'}), 403
    
    return jsonify({'image_url': post.image_url}), 200

@app.route('/groups/<int:group_id>/challenge', methods=['GET'])
@token_required
def get_daily_challenge(current_user, group_id):
    if not verify_group_membership(current_user, group_id):
        return jsonify({'error': 'User is not a member of this group'}), 403
    
    today = date.today()
    challenge = DailyChallenge.query.filter_by(
        group_id=group_id,
        challenge_date=today
    ).first()
    
    if not challenge:
        return jsonify({'error': 'No challenge for today'}), 404
    
    return jsonify({
        'id': challenge.id,
        'start_time': challenge.start_time.isoformat(),
        'end_time': challenge.end_time.isoformat(),
        'completed_users': challenge.completed_users
    })