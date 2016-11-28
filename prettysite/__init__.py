import os
from flask import Flask
import config as config
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_url_path='')

db = SQLAlchemy(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'prettyunit.db')

import models
import views




