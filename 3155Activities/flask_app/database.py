from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db

# Initialize the Flask-SQLAlchemy extension instance
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all() # run under the app context



