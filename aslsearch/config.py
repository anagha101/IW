import os

password = os.environ.get('DB_PASSWORD')

class Config:
    SECRET_KEY = 'asl_search_iw_app'
    # SQLALCHEMY_DATABASE_URI ='sqlite:///site.db'
    # if os.environ.get('DATABASE_URL'):
        # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
        # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        # SQLALCHEMY_DATABASE_URI = 'postgres://zxcztxnsiaqmcs:bba59de47e28686189bbff3accfaa503cf44e979cb27c1f8a3b5e8d2bc8dbeff@ec2-3-229-161-70.compute-1.amazonaws.com:5432/d5c55gh1c6l45j'
    # else:
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{password}@localhost/aslsearch'
        # SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'development'
    DEBUG = True
    TESTING = True