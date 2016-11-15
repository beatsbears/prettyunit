import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='')

db = SQLAlchemy(app)

import models
import views


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'prettyunit.db')
app.config['DEBUG'] = False
app.config['VERSION'] = '0.1-ALPHA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['LOG_PATH'] = os.path.join(basedir, 'logs/prettyunit.log')



