from flask import Flask, render_template, request, url_for

from prettysite import app, db
from models import Suite, TestCase, Test, Server
from APIValidation import APIHandler

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('index.html')

@app.route('/version')
def version():
    return render_template('index.html')

@app.route('/api/results', methods=['POST'])
def add_results():
    APIV = APIHandler()
    content = request.get_json(silent=True)

    # Parse Server
    APIV.server_parser(content)
    # Parse Suite
    APIV.suite_parser(content)
    # Parse TestCases and Tests
    APIV.tests_parser(content)
    return ('', 200)