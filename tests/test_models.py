import pytest
from app.models import User, Post, Comment, Like, Category
from datetime import datetime

def test_user_creation(test_user):
    assert test_user.username == 'testuser'
    assert test_user.email == 'test@example.com'
    assert test_user.check_password('password')

def test_post_creation(test_user):
    post = Post(title='Test Post', content='Test Content', author=test_user)
    assert post.title == 'Test Post'
    assert post.content == 'Test Content'
    assert post.author == test_user
    assert isinstance(post.created_at, datetime)

def test_comment_creation(test_user, test_post):
    comment = Comment(content='Test Comment', author=test_user, post=test_post)
    assert comment.content == 'Test Comment'
    assert comment.author == test_user
    assert comment.post == test_post
    assert isinstance(comment.created_at, datetime)

def test_like_creation(test_user, test_post):
    like = Like(user=test_user, post=test_post)
    assert like.user == test_user
    assert like.post == test_post
    assert isinstance(like.created_at, datetime)

def test_category_creation():
    category = Category(name='Test Category')
    assert category.name == 'Test Category'

def test_post_category_relationship(test_user):
    category = Category(name='Test Category')
    post = Post(title='Test Post', content='Test Content', author=test_user, category=category)
    assert post.category == category
    assert post in category.posts

def test_user_posts_relationship(test_user):
    post1 = Post(title='Post 1', content='Content 1', author=test_user)
    post2 = Post(title='Post 2', content='Content 2', author=test_user)
    assert post1 in test_user.posts
    assert post2 in test_user.posts

def test_user_comments_relationship(test_user, test_post):
    comment1 = Comment(content='Comment 1', author=test_user, post=test_post)
    comment2 = Comment(content='Comment 2', author=test_user, post=test_post)
    assert comment1 in test_user.comments
    assert comment2 in test_user.comments

def test_user_likes_relationship(test_user, test_post):
    like = Like(user=test_user, post=test_post)
    assert like in test_user.likes

def test_post_comments_relationship(test_user, test_post):
    comment1 = Comment(content='Comment 1', author=test_user, post=test_post)
    comment2 = Comment(content='Comment 2', author=test_user, post=test_post)
    assert comment1 in test_post.comments
    assert comment2 in test_post.comments

def test_post_likes_relationship(test_user, test_post):
    like = Like(user=test_user, post=test_post)
    assert like in test_post.likes

def test_user_bio():
    user = User(username='testuser', email='test@example.com')
    user.bio = 'Test bio'
    assert user.bio == 'Test bio'

def test_post_updated_at(test_user):
    post = Post(title='Test Post', content='Test Content', author=test_user)
    assert post.updated_at == post.created_at
    # Note: Testing updated_at changes would require database interaction 