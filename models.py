"""Models for Therapist app."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref,relationship
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Therapist(db.Model):
    """Therapist."""
    __tablename__ = "therapists"

    therapistID = db.Column(db.Integer,primary_key=True,nullable =False,)            
    first_name = db.Column(db.String(30), 
                         nullable=False)
    last_name = db.Column(db.String(30), 
                         nullable=False)
    address = db.Column(db.Text,nullable = False)
    phone = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    speciality = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    startDay = db.Column(db.String(9),)
    endDay = db.Column(db.String(9),)
    startTime = db.Column(db.String(8),)
    endTime = db.Column(db.String(8),)
    schedules = relationship("Schedule", back_populates="therapist")
    
    def to_dict(self):
        """Serialize Therapist to a dict of therapist info."""

        return {
            
            "Firs_name": self.first_name,
            "Last_name": self.last_name,
            "Address": self.address,
            "Phone": self.phone,
            
            "speciality" : self.speciality,
            "Start_day" : self.startDay,
            "End_day" : self.endDay,
            "Start_time" : self.startTime,
            "End_time" : self.endTime,
        }
    
    

class Patient(db.Model):
    """Patient."""
    __tablename__ = "patients"

    patientID = db.Column(db.Integer,primary_key=True,nullable =False,)
    first_name = db.Column(db.String(30), 
                         nullable=False)
    last_name = db.Column(db.String(30), 
                         nullable=False)
    address = db.Column(db.Text,nullable = False)
    phone = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    payment= db.relationship('Payment',cascade='all,delete',backref='patients')
    schedule=db.relationship('Schedule',cascade='all,delete',backref='patients')
    schedules = db.relationship("Schedule", back_populates="patient")
   
    def to_dict(self):
        """Serialize Patient to a dict of patient info."""

        return {
            
            "Firs_name": self.first_name,
            "Last_name": self.last_name,
            "Address": self.address,
            "Phone": self.phone,
            
        }
    

class User(db.Model):
    """Users."""
    __tablename__ = "users"
    userID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)               
    username = db.Column(db.Text,
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



class Schedule(db.Model):
    """Schedule."""
    __tablename__ = "schedules"

    scheduleID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)              
    patientID = db.Column(db.Integer,
                   db.ForeignKey('patients.patientID'),nullable =False,)
    therapistID = db.Column(db.Integer,
                   db.ForeignKey('therapists.therapistID'),nullable =False,)
    day =db.Column(db.String(11), nullable = False,) 
    time = db.Column(db.String(5),nullable = False,)
    frequency = db.Column(db.String(20)) 
    status = db.Column(db.String(40),
                     nullable=False,
                     unique=False)
    comments = db.Column(db.Text, 
                        nullable=True)
    patient = db.relationship("Patient", back_populates="schedules")
    therapist = db.relationship("Therapist", back_populates="schedules")
    

    class Payment(db.Model):
    """Payment."""
    __tablename__ = "payments"

    paymentID = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    patientID =   db.Column(db.Integer,
                   db.ForeignKey('patients.patientID'),unique=False,  nullable =False,)            
    amount = db.Column(db.Integer,
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
                     unique=False)
 

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)
