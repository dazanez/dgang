from flask import Flask, request, jsonify
from firebase_admin import auth
import jwt
from datetime import datetime, timedelta
from functools import wraps
from .config import JWT_SECRET_KEY, JWT_EXPIRATION_HOURS, FLASK_HOST, FLASK_PORT
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = auth.get_user(data['uid'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Create user in Firebase
        user = auth.create_user(
            email=email,
            password=password
        )
        
        # Generate JWT token with sub claim
        token = jwt.encode({
            'uid': user.uid,
            'sub': user.uid,  # Add the sub claim
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        }, JWT_SECRET_KEY)

        return jsonify({
            'message': 'Successfully registered',
            'token': token,
            'user': {
                'uid': user.uid,
                'email': user.email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Verify the user credentials with Firebase
        user = auth.get_user_by_email(email)
        
        # Generate JWT token with sub claim
        token = jwt.encode({
            'uid': user.uid,
            'sub': user.uid,  # Add the sub claim
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        }, JWT_SECRET_KEY)
        
        return jsonify({
            'token': token,
            'user': {
                'uid': user.uid,
                'email': user.email
            }
        })
        
    except Exception as e:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/auth/user', methods=['GET'])
@token_required
def get_user(current_user):
    return jsonify({
        'uid': current_user.uid,
        'email': current_user.email
    })

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)