from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError

from database import db
import datetime

class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    # can create a foreign key; referencing the id variable in the User class,
    # so that is why it is lowercase
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title, text, date, user_id):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = user_id

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    notes = db.relationship("Note", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()

class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [Email(message='Not a valid email address.'), DataRequired()])

    password = PasswordField('Password', [DataRequired(message='Please enter a password.')])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password')
