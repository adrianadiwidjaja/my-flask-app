from setuptools import setup, find_packages

setup(
    name="flask_blog",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.2',
        'Flask-SQLAlchemy==3.1.1',
        'Flask-Login==0.6.3',
        'Flask-WTF==1.2.1',
        'python-dotenv==1.0.1',
        'Werkzeug==3.0.1',
        'email-validator==2.1.0.post1',
        'pytest==8.0.0',
        'pytest-cov==4.1.0',
        'pytest-flask==1.3.0'
    ],
) 