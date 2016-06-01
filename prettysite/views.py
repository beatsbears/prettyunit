from flask import Flask, render_template, request, url_for

from prettysite import app, db
from models import Suite, TestCase, Tests, Server

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('index.html')

@app.route('/version')
def version():
    return render_template('index.html')
