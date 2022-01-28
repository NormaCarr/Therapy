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
# 

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Patient.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.loginID

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def home_page():
    return render_template('base.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = SignupAddForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('/login.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

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
        return redirect(f'/patientInfo/{user.loginID}')
    return render_template('/signup.html', form=form)


@app.route('/patientInfo/<int:user_id>', methods=["GET", "POST"])
def patientInfo(user_id):
    "Form to fill patient's information"

    
    form=PatientAddForm()
    
    if user_id != session[CURR_USER_KEY]:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    if form.validate_on_submit():
         try:
            user=Patient(userID=user_id,first_name = form.first_name.data,
                         last_name = form.last_name.data,
                         email = form.email.data,
                         phone = form.phone.data,
                         address = form.address.data,)
            db.session.add(user)
            db.session.commit()
            return redirect(f"/showpatient/{user.patientID}")
         except IntegrityError:
            #db.session.rollback()
            flash("Email related to another account", 'danger')    
            return render_template('/patientInfo.html',form=form) 
    
    return render_template('/patientInfo.html',form=form)
    
@app.route('/showpatient/<int:user_id>')
def show_patient_inf(user_id):
       
    if user_id != session[CURR_USER_KEY]:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = Patient.query.get_or_404(user_id)
    form=PatientAddForm() 
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email
    form.phone.data = user.phone
    form.address.data = user.address 
    return render_template('/showpatient.html', form=form)


@app.route('/logout')
def logout():
   """Handle logout of user."""
   do_logout()
   return redirect("/")