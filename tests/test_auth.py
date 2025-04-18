import pytest
from app import db
from app.models import User, Post
from flask import url_for
from datetime import datetime

def test_login_route(client, init_database):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Sign In' in response.data

def test_login_success(client, init_database):
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to Flask App' in response.data

def test_login_failure(client, init_database):
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

def test_register_route(client, init_database):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_success(client, init_database):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful!' in response.data

def test_register_duplicate_email(client, init_database):
    response = client.post('/auth/register', data={
        'username': 'anotheruser',
        'email': 'test@example.com',  # Already exists
        'password': 'newpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email already registered' in response.data

def test_logout(auth_client, init_database):
    response = auth_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to Flask App' in response.data
    # Verify user is logged out by trying to access protected route
    response = auth_client.get('/create_post')
    assert response.status_code == 302  # Redirect to login
    assert '/auth/login' in response.location

def test_login(client, auth):
    response = auth.login()
    assert response.status_code == 200
    assert b'Logout' in response.data

def test_logout(client, auth):
    auth.login()
    response = auth.logout()
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register(client, auth):
    response = auth.register(username='newuser', email='new@example.com', password='password')
    assert response.status_code == 200
    assert User.query.filter_by(username='newuser').first() is not None

def test_profile_page(client, auth, test_user):
    auth.login()
    response = client.get(url_for('auth.profile'))
    assert response.status_code == 200
    assert b'Your Profile' in response.data
    assert test_user.username.encode() in response.data

def test_edit_profile(client, auth, test_user):
    auth.login()
    response = client.post(url_for('auth.edit_profile'),
                         data={'username': 'updateduser',
                              'email': 'updated@example.com',
                              'bio': 'New bio'},
                         follow_redirects=True)
    assert response.status_code == 200
    updated_user = User.query.get(test_user.id)
    assert updated_user.username == 'updateduser'
    assert updated_user.email == 'updated@example.com'
    assert updated_user.bio == 'New bio'

def test_change_password(client, auth, test_user):
    auth.login()
    response = client.post(url_for('auth.edit_profile'),
                         data={'username': test_user.username,
                              'email': test_user.email,
                              'new_password': 'newpassword'},
                         follow_redirects=True)
    assert response.status_code == 200
    updated_user = User.query.get(test_user.id)
    assert updated_user.check_password('newpassword')

def test_user_profile_page(client, test_user, test_post):
    response = client.get(url_for('auth.user_profile', username=test_user.username))
    assert response.status_code == 200
    assert test_user.username.encode() in response.data
    assert test_post.title.encode() in response.data

def test_profile_pagination(client, auth, test_user):
    # Create multiple posts
    for i in range(6):
        post = Post(title=f'Profile Post {i}', content=f'Content {i}', author=test_user)
        db.session.add(post)
    db.session.commit()
    
    auth.login()
    # Test first page
    response = client.get(url_for('auth.profile'))
    assert response.status_code == 200
    assert b'Profile Post 0' in response.data
    assert b'Profile Post 4' in response.data
    assert b'Profile Post 5' not in response.data
    
    # Test second page
    response = client.get(url_for('auth.profile', page=2))
    assert response.status_code == 200
    assert b'Profile Post 5' in response.data
    assert b'Profile Post 0' not in response.data

def test_duplicate_username_registration(client, auth, test_user):
    response = auth.register(username=test_user.username,
                           email='different@example.com',
                           password='password')
    assert response.status_code == 200
    assert b'Username already taken' in response.data

def test_duplicate_email_registration(client, auth, test_user):
    response = auth.register(username='differentuser',
                           email=test_user.email,
                           password='password')
    assert response.status_code == 200
    assert b'Email already registered' in response.data

def test_invalid_login(client, auth):
    response = auth.login(email='wrong@example.com', password='wrongpassword')
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data 