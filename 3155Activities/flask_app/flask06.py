

# imports
import os   # os is used to get environment variables IP & PORT
from flask import Flask
from flask import render_template
from flask import request
from datetime import date
from flask import redirect, url_for
from models import Note as Note, LoginForm
from models import User as User
from database import db
from forms import RegisterForm
import bcrypt
from flask import session



app = Flask(__name__)   # initialize Flask app, this is the Web App we will be customizing

#Configure the database connection by setting the name and
# location of the database file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'

# disable an unneeded feature for us of Flask-SQLAlchemy that signals the
# application every time a change is about to be made in the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure secret key that will be used by the app to secure session data:
app.config['SECRET_KEY'] = 'SE3155'

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')    # Landing page
def index():
    # check if a user is saved in session
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template("index.html")


@app.route('/notes')    # View page with all notes
def get_notes():

    # check if a user is saved in session
    if session.get('user'):
        # retrieve notes from database
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        return redirect(url_for('login'))



@app.route('/note/<note_id>')   # View individual note
def get_note(note_id):
    # retrieve user from database
    stephenUser = db.session.query(User).filter_by(email='szargo@uncc.edu').one()
    # retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note = my_note, user = stephenUser)

@app.route('/notes/new', methods = ['GET', 'POST']) # Post a new note page
def new_note():

    if session.get('user'):
        # check method used for request
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
            new_record = Note(title, text, today, session['user_id'])
            # add the newly created Note object to database
            db.session.add(new_record)
            db.session.commit()

            # render response - redirect to notes listing
            return redirect(url_for('get_notes'))
        else:
            # GET request - show new note page
            # retrieve user from database
            return render_template('new.html', user=session['user'])
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])   # edit existing note page
def update_note(note_id):
    # check method used for request
    if session.get('user'):
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get note data
            text = request.form['noteText']
            note = db.session.query(Note).filter_by(id=note_id).one()
            # update note data
            note.title = title
            note.text = text
            # update note in Database
            db.session.add(note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            # GET request - show new note form to edit note
            # retrieve note from database
            my_note = db.session.query(Note).filter_by(id=note_id).one()

            return render_template('new.html', note = my_note, user = session['user'])
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    if session.get('user'):
        # retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()
        db.session.delete(my_note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        # user is not in sesssion redirect to login
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)



app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
