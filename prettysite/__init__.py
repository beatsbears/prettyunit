from flask import Flask
import config as config
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_url_path='')

db = SQLAlchemy(app)

import models
import views



