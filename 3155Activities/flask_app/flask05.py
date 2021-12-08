

# imports
import os   # os is used to get environment variables IP & PORT
from flask import Flask
from flask import render_template
from flask import request
from datetime import date
from flask import redirect, url_for
from models import Note as Note
from models import User as User
from database import db



app = Flask(__name__)   # initialize Flask app, this is the Web App we will be customizing

#Configure the database connection by setting the name and
# location of the database file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'

# disable an unneeded feature for us of Flask-SQLAlchemy that signals the
# application every time a change is about to be made in the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/index')    # Landing page
def index():
    # get user from database
    stephenUser =  db.session.query(User).filter_by(email='szargo@uncc.edu').one()
    return render_template("index.html", user = stephenUser)

@app.route('/notes')    # View page with all notes
def get_notes():
    # retrieve user from database
    stephenUser = db.session.query(User).filter_by(email='szargo@uncc.edu').one()
    # retrieve notes from database
    my_notes = db.session.query(Note).all()
    return render_template('notes.html', notes = my_notes, user = stephenUser)

@app.route('/note/<note_id>')   # View individual note
def get_note(note_id):
    # retrieve user from database
    stephenUser = db.session.query(User).filter_by(email='szargo@uncc.edu').one()
    # retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note = my_note, user = stephenUser)

@app.route('/notes/new', methods = ['GET', 'POST']) # Post a new note page
def new_note():
    print('request method is ', request.method)
    if request.method == 'POST':

        # get title data
        title = request.form['title']
        # get note data
        text = request.form['noteText']
        # create date stamp
        today = date.today()
        # format date mm/dd/yyyy
        today = today.strftime("%m-%d-%Y")
        # create the new Note object from data inputted
        new_record = Note(title, text, today)
        # add the newly created Note object to database
        db.session.add(new_record)
        db.session.commit()

        # render response - redirect to notes listing
        return redirect(url_for('get_notes'))
    else:
        # GET request - show new note page
        # retrieve user from database
        stephenUser = db.session.query(User).filter_by(email = 'szargo@uncc.edu').one()
        return render_template('new.html', user = stephenUser)

@app.route('/notes/edit/<note_id>')   # edit existing note page
def update_note(note_id):
    # retrieve user from database
    stephenUser = db.session.query(User).filter_by(email='szargo@uncc.edu').one()
    # retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('new.html', note = my_note, user = stephenUser)



app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
