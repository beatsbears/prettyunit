import os


basedir = os.path.abspath(os.path.dirname(__file__))



SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'prettyunit.db')
DEBUG = False
VERSION = '0.1-ALPHA'
SQLALCHEMY_TRACK_MODIFICATIONS = True
LOG_PATH = os.path.join(basedir, 'logs/prettyunit.log')
