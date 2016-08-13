import os

from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'prettyunit.db')
app.config['DEBUG'] = True
app.config['VERSION'] = '0.1-ALPHA'
db = SQLAlchemy(app)

import models
import views
