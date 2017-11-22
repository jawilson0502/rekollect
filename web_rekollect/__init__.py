import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db

app = Flask(__name__)

import web_rekollect.views
import yaml

CONFIG_FILE_NAME = 'config.yaml'
with open(CONFIG_FILE_NAME, 'r') as f:
    DB_CONFIG = yaml.load(f)['postgres']

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
