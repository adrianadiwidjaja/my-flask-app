import pytest
from app import create_app, db
from app.models import User, Post, Category

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='test@example.com', password='password'):
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password, 'remember_me': False},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/auth/logout', follow_redirects=True)

    def register(self, username='testuser', email='test@example.com', password='password'):
        return self._client.post(
            '/auth/register',
            data={'username': username, 'email': email, 'password': password},
            follow_redirects=True
        )

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        # Refresh the user to ensure it's attached to the session
        db.session.refresh(user)
        return user

@pytest.fixture
def test_post(app, test_user):
    with app.app_context():
        post = Post(title='Test Post', content='Test Content', author=test_user)
        db.session.add(post)
        db.session.commit()
        # Refresh the post to ensure it's attached to the session
        db.session.refresh(post)
        return post

@pytest.fixture
def test_category(app):
    with app.app_context():
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()
        # Refresh the category to ensure it's attached to the session
        db.session.refresh(category)
        return category

@pytest.fixture
def auth_client(client, test_user):
    with client:
        client.post('/auth/login', data={
            'email': test_user.email,
            'password': 'password'
        })
        yield client 