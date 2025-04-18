import pytest
from flask import url_for
from app import db
from app.models import Post, Comment, Like, Category, User
from datetime import datetime

def test_index_route(client, init_database):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Flask App' in response.data
    assert b'Test Post' in response.data

def test_create_post_unauthorized(client, init_database):
    response = client.get('/create_post')
    assert response.status_code == 302  # Redirect to login
    assert '/auth/login' in response.location

def test_create_post_authorized(auth_client, init_database):
    response = auth_client.get('/create_post')
    assert response.status_code == 200
    assert b'Create New Post' in response.data

    # Test post creation
    response = auth_client.post('/create_post', data={
        'title': 'New Test Post',
        'content': 'This is a new test post'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'New Test Post' in response.data
    assert b'Your post has been created!' in response.data

def test_create_post_invalid_data(auth_client, init_database):
    response = auth_client.post('/create_post', data={
        'title': '',  # Empty title
        'content': 'This is a test post'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Title and content are required!' in response.data

def test_index_page(client, test_post):
    response = client.get(url_for('main.index'))
    assert response.status_code == 200
    assert b'Test Post' in response.data

def test_create_post(client, auth, test_user):
    auth.login()
    response = client.post(url_for('main.create_post'),
                         data={'title': 'New Post', 'content': 'New Content'},
                         follow_redirects=True)
    assert response.status_code == 200
    assert b'New Post' in response.data
    assert Post.query.filter_by(title='New Post').first() is not None

def test_edit_post(client, auth, test_post):
    auth.login()
    response = client.post(url_for('main.edit_post', post_id=test_post.id),
                         data={'title': 'Updated Post', 'content': 'Updated Content'},
                         follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Post' in response.data
    assert Post.query.get(test_post.id).title == 'Updated Post'

def test_delete_post(client, auth, test_post):
    auth.login()
    response = client.post(url_for('main.delete_post', post_id=test_post.id),
                         follow_redirects=True)
    assert response.status_code == 200
    assert Post.query.get(test_post.id) is None

def test_comment_post(client, auth, test_post):
    auth.login()
    response = client.post(url_for('main.comment_post', post_id=test_post.id),
                         data={'content': 'Test Comment'},
                         follow_redirects=True)
    assert response.status_code == 200
    assert Comment.query.filter_by(content='Test Comment').first() is not None

def test_like_post(client, auth, test_post):
    auth.login()
    response = client.post(url_for('main.like_post', post_id=test_post.id),
                         follow_redirects=True)
    assert response.status_code == 200
    assert Like.query.filter_by(post_id=test_post.id).first() is not None

def test_unlike_post(client, auth, test_post):
    auth.login()
    # First like the post
    client.post(url_for('main.like_post', post_id=test_post.id))
    # Then unlike it
    response = client.post(url_for('main.like_post', post_id=test_post.id),
                         follow_redirects=True)
    assert response.status_code == 200
    assert Like.query.filter_by(post_id=test_post.id).first() is None

def test_category_posts(client, test_post, test_category):
    test_post.category = test_category
    response = client.get(url_for('main.category_posts', category_id=test_category.id))
    assert response.status_code == 200
    assert b'Test Post' in response.data

def test_post_pagination(client, test_user):
    # Create multiple posts
    for i in range(6):
        post = Post(title=f'Post {i}', content=f'Content {i}', author=test_user)
        db.session.add(post)
    db.session.commit()
    
    # Test first page
    response = client.get(url_for('main.index'))
    assert response.status_code == 200
    assert b'Post 0' in response.data
    assert b'Post 4' in response.data
    assert b'Post 5' not in response.data
    
    # Test second page
    response = client.get(url_for('main.index', page=2))
    assert response.status_code == 200
    assert b'Post 5' in response.data
    assert b'Post 0' not in response.data

def test_unauthorized_post_edit(client, auth, test_post):
    # Create a different user
    other_user = User(username='otheruser', email='other@example.com')
    other_user.set_password('password')
    db.session.add(other_user)
    db.session.commit()
    
    # Login as other user
    auth.login(email='other@example.com', password='password')
    
    # Try to edit the post
    response = client.post(url_for('main.edit_post', post_id=test_post.id),
                         data={'title': 'Unauthorized Edit', 'content': 'Unauthorized Content'},
                         follow_redirects=True)
    assert response.status_code == 403
    assert Post.query.get(test_post.id).title == 'Test Post'  # Post should not be changed 