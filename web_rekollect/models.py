from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import yaml

db = SQLAlchemy()

class Files(db.Model):
    '''Model for all the uploaded files'''
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    file_name = db.Column(db.String, nullable=False)

class Results(db.Model): 
    '''Model for results from Rekollect'''
    __tablename__ = 'results'

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    plugin = db.Column(db.String, nullable=False)
    result = db.Column(db.JSON, nullable=False)
