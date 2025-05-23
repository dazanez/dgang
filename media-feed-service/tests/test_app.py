import os
import pytest
from datetime import datetime, date
from src.app import app, db
from src.models import Post, DailyChallenge
from io import BytesIO

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            
        # Cleanup
        db.session.remove()
        db.drop_all()

def test_create_post(client, mocker):
    # Mock JWT verification
    mocker.patch('jwt.decode', return_value={'user_id': 1})
    # Mock group membership verification
    mocker.patch('src.app.verify_group_membership', return_value=True)
    
    data = {
        'group_id': '1',
        'caption': 'Test post',
        'image_url': 'https://example.com/image.jpg'
    }
    
    response = client.post(
        '/posts',
        json=data,
        headers={'Authorization': 'Bearer test-token'},
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['caption'] == 'Test post'

def test_get_group_feed(client, mocker):
    # Mock JWT verification
    mocker.patch('jwt.decode', return_value={'user_id': 1})
    # Mock group membership verification
    mocker.patch('src.app.verify_group_membership', return_value=True)
      # Create test posts
    posts = [
        Post(user_id=1, group_id=1, image_url='https://example.com/test1.jpg', caption='Test 1'),
        Post(user_id=1, group_id=1, image_url='https://example.com/test2.jpg', caption='Test 2')
    ]
    with app.app_context():
        db.session.add_all(posts)
        db.session.commit()
    
    response = client.get(
        '/groups/1/feed',
        headers={'Authorization': 'Bearer test-token'}
    )
    
    assert response.status_code == 200
    assert len(response.json['posts']) == 2
    assert response.json['total'] == 2

def test_get_daily_challenge(client, mocker):
    # Mock JWT verification
    mocker.patch('jwt.decode', return_value={'user_id': 1})
    # Mock group membership verification
    mocker.patch('src.app.verify_group_membership', return_value=True)
    
    # Create test challenge
    challenge = DailyChallenge(
        group_id=1,
        challenge_date=date.today(),
        start_time=datetime.now(),
        end_time=datetime.now(),
        completed_users=[1, 2]
    )
    with app.app_context():
        db.session.add(challenge)
        db.session.commit()
    
    response = client.get(
        '/groups/1/challenge',
        headers={'Authorization': 'Bearer test-token'}
    )
    
    assert response.status_code == 200
    assert response.json['completed_users'] == [1, 2]

def test_unauthorized_access(client):
    response = client.get('/groups/1/feed')
    assert response.status_code == 401
    
    response = client.get('/groups/1/feed', headers={'Authorization': 'Bearer invalid-token'})
    assert response.status_code == 401

def test_non_member_access(client, mocker):
    # Mock JWT verification
    mocker.patch('jwt.decode', return_value={'user_id': 1})
    # Mock group membership verification to deny access
    mocker.patch('src.app.verify_group_membership', return_value=False)
    
    response = client.get(
        '/groups/1/feed',
        headers={'Authorization': 'Bearer test-token'}
    )
    assert response.status_code == 403