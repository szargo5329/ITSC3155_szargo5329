# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request


app = Flask(__name__)     # create an app
stephenUser = {'name': 'Stephen', 'email':'szargo@uncc.edu'}

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/index')
def index():

    return render_template("index.html" , user = stephenUser)

@app.route('/notes')
def get_notes():
    notes = {
        1: {'title':'First note', 'text':'This is my first note', 'date':'10-1-2020'},
        2: {'title':'Second note', 'text':'This is my second note', 'date':'10-2-2020'},
        3: {'title':'Third note', 'text':'This is my third note', 'date':'10-3-2020'}
    }
    return render_template('notes.html', notes = notes, user = stephenUser)

@app.route('/note/<note_id>')
def get_note(note_id):
    notes = {
        1: {'title':'First note', 'text':'This is my first note', 'date':'10-1-2020'},
        2: {'title':'Second note', 'text':'This is my second note', 'date':'10-2-2020'},
        3: {'title':'Third note', 'text':'This is my third note', 'date':'10-3-2020'}
    }
    return render_template('note.html', note = notes[int(note_id)], user = stephenUser)

@app.route('/notes/new', methods = ['GET', 'POST'])
def new_note():
    print('request method is ', request.method)
    if request.method == 'POST':
        request_data = request.form
        return f"data: {request_data} !"
    else:
        return render_template('new.html', user = stephenUser)



app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
