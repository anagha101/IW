# ----------------------------------------------------------------------
# config.py
# Author: Anagha Rajagopalan
# ----------------------------------------------------------------------
import os
# ----------------------------------------------------------------------

password = os.environ.get('DB_PASSWORD')

class Config:
    SECRET_KEY = 'asl_search_iw_app'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
    # SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{password}@localhost/aslsearchdb'
    SQLALCHEMY_DATABASE_URI ='sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'development'
    TESTING = True