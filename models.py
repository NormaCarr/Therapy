"""Models for Therapist app."""
from datetime import datetime

from flask_bcrypt import Bcrypt
from pickle import TRUE
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()
bcrypt = Bcrypt()

class Therapist(db.Model):
    """Therapist."""
    __tablename__ = "therapists"

    therapistID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    userID =db.Column(db.Integer,
                 db.ForeignKey('users.loginID'),nullable =False,)
    first_name = db.Column(db.String(30), 
                         nullable=False)
    last_name = db.Column(db.String(30), 
                         nullable=False)
    address = db.Column(db.Text,nullable = False)
    phone = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    email = db.Column(db.String(50), 
                         nullable=False,unique=TRUE)
    speciality = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    

class Patient(db.Model):
    """Patient."""
    __tablename__ = "patients"

    patientID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    userID = db.Column(db.Integer,
                   db.ForeignKey('users.loginID'),nullable =False,)
    first_name = db.Column(db.String(30), 
                         nullable=False)
    last_name = db.Column(db.String(30), 
                         nullable=False)
    address = db.Column(db.Text,nullable = False)
    phone = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    email = db.Column(db.String(50), 
                         nullable=False,unique=TRUE)
    
    

class User(db.Model):
    """Users."""
    __tablename__ = "users"
    loginID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20),
                        nullable=False,unique=True,)
    password = db.Column(db.Text, 
                        nullable=False)
    
    @classmethod
    def signup(cls, username, password):
        """Sign up user patient.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        login = User(
            username=username,
            password=hashed_pwd,    
        )

        db.session.add(login)
        return login
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Session(db.Model):
    """Session."""
    __tablename__ = "sessions"

    sessionID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    paymentID = db.Column(db.Integer,
                   db.ForeignKey('payments.paymentID'),nullable =False,)
    calendarID = db.Column(db.Integer,
                   db.ForeignKey('calendars.calendarID'),nullable =False,)
    status = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    

class Schedule(db.Model):
    """Schedule."""
    __tablename__ = "schedules"

    scheduleID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    therapistID = db.Column(db.Integer,
                   db.ForeignKey('therapists.therapistID'),nullable =False,)
    patientID = db.Column(db.Integer,
                   db.ForeignKey('patients.patientID'),nullable =False,)
    sessionID = db.Column(db.Integer,
                   db.ForeignKey('sessions.sessionID'),nullable =False,)
    date =db.Column(db.DateTime,nullable =False,) 
    status = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    
class Payment(db.Model):
    """Payment."""
    __tablename__ = "payments"

    paymentID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    amount = db.Column(db.Float,
                     nullable=False,
                     unique=False)
    date =db.Column(db.DateTime,
                     nullable=False,
                     unique=False)
    concept = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    card = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    
class Calendar(db.Model):
    "Calendar""."""
    __tablename__ = "calendars"

    calendarID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    sessionID = db.Column(db.Integer,db.ForeignKey('sessions.sessionID'),nullable =False,)
    date = db.Column(db.DateTime, nullable =False,)
    status = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)