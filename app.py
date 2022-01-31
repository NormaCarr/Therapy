from concurrent.futures.process import _python_exit
import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import TherapistAddForm,SignupAddForm, UserAddForm, PatientAddForm
from models import db, connect_db, Therapist, Patient,User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:metal@localhost:5432/therapist'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
#toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


##############################################################################
#          Basic operations for all users Login, Logout, Sign up. 

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.userID

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def verifyAccount(user):
    """Verify is the account is from a patient or therapist"""
    if Therapist.query.get(user.userID):
      return "therapist"
    return "patient"

@app.route('/therapist')
def home_page_therapist():
    return render_template('/therapist/therapistHome.html')

@app.route('/patient')
def home_page_patient():
    return render_template('/patient/patientHome.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = SignupAddForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            
            account=verifyAccount(user)
            return redirect(f"/{account}")

        flash("Invalid credentials.", 'danger')

    return render_template('/login.html', form=form)

@app.route('/logout')
def logout():
   """Handle logout of user."""
   user=g.user
   account=verifyAccount(user)
   do_logout()
   return redirect(f"/{account}")
   

  
#################### Patient ##################################

@app.route('/patient/signup', methods=["GET", "POST"])
def signupPatient():
    """Handle patient signup.

    Create new user patient and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = SignupAddForm()
    
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data)
            db.session.commit() 
            
        except IntegrityError:
            #db.session.rollback()
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)
        
        do_login(user)
        return redirect(f"/patient/patientInfo/{user.userID}")
    return render_template('/signup.html', form=form)


@app.route('/patient/patientInfo/<int:user_id>', methods=["GET", "POST"])
def patientInfo(user_id):
    "Form to fill patient's information"
   
    form=PatientAddForm()    
    if user_id != session[CURR_USER_KEY]:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    if form.validate_on_submit():
         try:
            user=Patient(patientID=user_id,first_name = form.first_name.data,
                         last_name = form.last_name.data,
                         email = form.email.data,
                         phone = form.phone.data,
                         address = form.address.data,)
            db.session.add(user)
            db.session.commit()
            return redirect(f"/patient/showPatient/{user.patientID}")
         except IntegrityError:
            #db.session.rollback()
            flash("Email related to another account", 'danger')    
            return render_template('/patient/patientInfo.html',form=form) 
    
    return render_template('/patient/patientInfo.html',form=form)
    

@app.route('/patient/showPatient/<int:user_id>')
def show_patient_inf(user_id):
       
    if user_id != session[CURR_USER_KEY]:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = Patient.query.get_or_404(user_id)
    if user:
       form=PatientAddForm(obj=user) 
    
    return render_template('/patient/showPatient.html', form=form)

@app.route('/patient/editPatient/<int:user_id>',methods=["GET","POST"])
def edit_patient(user_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/patient")
    user = Patient.query.filter_by(patientID=user_id).first_or_404()
   
    form=PatientAddForm(obj=user)

    if form.validate_on_submit():
         try:
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.address = form.address.data
            
            db.session.commit()
            return redirect(f"/patient/showPatient/{user.patientID}")
         except IntegrityError:
            #db.session.rollback()
            flash("Email related to another account", 'danger')    
            return render_template('/patient/editPatient.html',form=form) 
    
    return render_template('/patient/editPatient.html',form=form)


#####################  Therapist ######################################

@app.route('/therapist/signup', methods=["GET", "POST"])
def signuptherapist():
    """Handle therapist signup.

    Create new user therapist and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = SignupAddForm()
    
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data)
            db.session.commit() 
            
        except IntegrityError:
            #db.session.rollback()
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)
        
        do_login(user)
        return redirect(f"/therapist/therapistInfo/{user.userID}")
    return render_template('/signup.html', form=form)


@app.route('/therapist/therapistInfo/<int:user_id>', methods=["GET", "POST"])
def therapistInfo(user_id):
    "Form to fill tharapist's information"
   
    form=TherapistAddForm()    
    if user_id != session[CURR_USER_KEY]:
        flash("Access unauthorized.", "danger")
        return redirect("/therapist")
    if form.validate_on_submit():
         try:
            user=Therapist(therapistID=user_id,first_name = form.first_name.data,
                         last_name = form.last_name.data,
                         email = form.email.data,
                         phone = form.phone.data,
                         address = form.address.data,
                         speciality=form.speciality.data)
            db.session.add(user)
            db.session.commit()
            return redirect(f"/therapist/showTherapist/{user_id}")
         except IntegrityError:
            #db.session.rollback()
            flash("Email related to another account", 'danger')    
            return render_template('/therapist/therapistInfo.html',form=form) 
    
    return render_template('/therapist/therapistInfo.html',form=form)

@app.route('/therapist/showTherapist/<int:user_id>')
def show_therapist_inf(user_id):
       
    if user_id != session[CURR_USER_KEY]:
        flash("Access unauthorized.", "danger")
        return redirect("/therapist")
    
    user = Therapist.query.filter_by(therapistID=user_id).first_or_404()
    form=TherapistAddForm(obj=user) 
    
    return render_template('/therapist/showTherapist.html', form=form)

@app.route('/therapist/editTherapist/<int:user_id>',methods=["GET","POST"])
def edit_therapist(user_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/therapist")
    user = Therapist.query.filter_by(therapistID=user_id).first_or_404()
   
    form=TherapistAddForm(obj=user)

    if form.validate_on_submit():
         try:
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.address = form.address.data
            
            db.session.commit()
            return redirect(f"/therapist/showTherapist/{user.therapistID}")
         except IntegrityError:
            #db.session.rollback()
            flash("Email related to another account", 'danger')    
            return render_template('/therapist/editTherapist.html',form=form) 
    
    return render_template('/therapist/editTherapist.html',form=form)