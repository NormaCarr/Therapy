

from datetime import datetime

import os

from flask import Flask, jsonify,render_template, request, flash, redirect, session, g
#from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.exc import IntegrityError

from utility_functions import verifyAccount,validateStartTime,currentDatetoArray,hideCardNumber,validAppDayTime,emailvalid
from forms import  LoginForm, PaymentForm,TherapistAddForm,SignupAddForm, PatientAddForm
from models import Payment, Schedule, db, connect_db, Therapist, Patient,User

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
#          Basic operations for all users Login, Logout, Sign up and validation. 



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


@app.route('/')
def primero():
    return render_template('/base.html')


@app.route('/therapist')
def home_page_therapist():
    return render_template('/therapist/therapistHome.html')

@app.route('/patient')
def home_page_patient():
    return render_template('/patient/patientHome.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            add_user_to_g()
            account=verifyAccount(user.userID)
            if account:
              return redirect(f"/{account}")

        flash("Invalid credentials.", 'danger')

    return render_template('/login.html', form=form)

@app.route('/logout')
def logout():
   """Handle logout of user."""
   user=g.user.userID
   account=verifyAccount(user)
   do_logout()
   return redirect(f"/{account}")
   
@app.route('/calendar')
def calendary():
    therapist=Therapist.query.all()
    now=datetime.now()
    now.year
    now.date
    return render_template('/therapist/calendar.html',info=therapist,date=now)
  
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
            if(emailvalid(form.username.data)=="DELIVERABLE"):    
                try:
                   user = User.signup(
                   username=form.username.data,
                   password=form.password.data)    
                except IntegrityError:
                  flash("Email related to another account", 'danger')
                  return render_template('/signup.html', form=form)
                db.session.commit()
                do_login(user)
                return redirect(f"/patient/patientInfo")
            else:
                flash(f"Invalid email, check the spelling")
    return render_template('/signup.html', form=form)


@app.route('/patient/patientInfo', methods=["GET", "POST"])
def patientInfo():
    "Form to fill patient's information"
    userID=g.user.userID
    form=PatientAddForm()    
    if not userID:
        flash("Access unauthorized.", "danger")
        return redirect("/patient")
    if form.validate_on_submit():
         
            user=Patient(patientID=userID,first_name = form.first_name.data,
                         last_name = form.last_name.data,
                        
                         phone = form.phone.data,
                         address = form.address.data,)
            db.session.add(user)
            db.session.commit()
            return redirect(f"/patient/showPatient")
           
    return render_template('/patient/patientInfo.html',form=form)
    

@app.route('/patient/showPatient')
def show_patient_inf():
    """Show patient's infromation"""  
    if (g.user.userID):
        user = Patient.query.get_or_404(g.user.userID)
        return render_template('/patient/showPatient.html', info=user.to_dict())
    else:        
       flash("Access unauthorized.", "danger")
       return redirect("/patient")
    


@app.route('/patient/editPatient',methods=["GET","POST"])
def edit_patient():
    """Update patien's information"""
    userID=g.user.userID
    user = Patient.query.filter_by(patientID=userID).first_or_404()
   
    form=PatientAddForm(obj=user)

    if form.validate_on_submit():
         
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.phone = form.phone.data
            user.address = form.address.data
            
            db.session.commit()
            return redirect(f"/patient/showPatient")
           
    return render_template('/patient/editPatient.html',form=form)

###--------------------  Appoint  --------------------------------###

@app.route('/patient/appoint')
def appointmentHTML():
    
    try:
        patSched=Schedule.query.filter_by(patientID=g.user.userID).first_or_404()
        return render_template('/schedule/appointment.html',appoint=patSched)
    except:
        date=currentDatetoArray()
        therapApp=Therapist.query.all()
        return render_template('/schedule/new_appointment.html',date=date,t_date=therapApp)
    

@app.route('/patient/new_appointment',methods=["POST"])
def new_appointment():
    """the appointment is added"""
    user=g.user.userID
    
    valDataApp=[request.form["day"],request.form["start_time"]]
    t_data=Therapist.query.all()
    valApp=validAppDayTime(valDataApp,t_data[0])
    if valApp:
           therap_ID=4 #therap_ID=4 comes from the proyect seed
           appoint=Schedule(patientID=user,therapistID=therap_ID,frequency="First_time",day=request.form["day"],time=request.form["start_time"],status = "To confirm",)
           db.session.add(appoint)
           db.session.commit()
           return redirect('/patient')
    flash("Date or time out of Therapist schedule", 'danger')
    return redirect('/patient/appoint')

@app.route('/patient/editAppoint')
def edit_appoint():    
        date=currentDatetoArray()
        therapApp=Therapist.query.all()
        return render_template('/schedule/edit_appointment.html',date=date,t_date=therapApp)

@app.route('/patient/modify_appointment',methods=["POST"])
def modify_appoint():  
    valDataApp=[request.form["day"],request.form["start_time"]]
    t_data=Therapist.query.all()
    valApp=validAppDayTime(valDataApp,t_data[0])
    if valApp:
       user=Schedule.query.filter_by(patientID=g.user.userID).first_or_404()
       user.day=request.form["day"]
       user.time=request.form["start_time"]
       db.session.commit()
       return redirect('/patient')
    flash("Date or time out of Therapist schedule", 'danger')      
    return redirect('/patient/editAppoint')


@app.route('/patient/cancelAppoint',methods=["GET"])
def cancel_appoint():
    """Delete appoint."""
    user=g.user.userID
    schedID=Schedule.query.filter_by(patientID=user).first_or_404()
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/patient")
    db.session.delete(schedID)
    db.session.commit()
    return redirect('/patient')

###--------------------------  Account  -----------------------###

@app.route('/patient/account')
def account():
    return render_template('/payment/account.html')

@app.route('/patient/listPayments')
def listPayments():
    #user=session[CURR_USER_KEY]
    user=g.user.userID
    payAccount=Payment.query.filter_by(patientID=user).all()
    if(payAccount):
        return render_template('/payment/listPayms.html',pay=payAccount)
    else:
         flash("There is not a payment")
         return render_template('/payment/account.html')

@app.route('/patient/payment', methods=["POST","GET"])
def payment():
    form=PaymentForm()  
    user=g.user.userID
    dt=datetime.now()
    date=str(dt.year)+'-'+str(dt.day)+'-'+str(dt.month)+' '+str(dt.hour)+':'+str(dt.minute)
    date = datetime.strptime(date, "%Y-%d-%m %H:%M")
    card=hideCardNumber(str(form.card.data))
    
    if form.validate_on_submit():
        pay=Payment(amount=form.amount.data,patientID=user,date=date,concept=form.concept.data,card=card,)    
        db.session.add(pay)
        db.session.commit()
        return redirect(f'/patient')
    return render_template('/payment/payment.html',form=form)

""" @app.route('/patient/payment/card', methods=["POST","GET"])
def paymentCard():
    return render_template('/payment/card.html') """
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
            flash("Email related to another account", 'danger')
            return render_template('/signup.html', form=form)
        
        do_login(user)
        return redirect(f"/therapist/therapistInfo")
    return render_template('/signup.html', form=form)

@app.route('/therapist/availability',methods=["GET","POST"])
def availability(): 
    
    user=Therapist.query.filter_by(therapistID=g.user.userID).first_or_404()
    if user:
      user.startDay=request.args.get("start_day")
      user.endDay=request.args.get("end_day")
      user.startTime=request.args.get("start_time")
      user.endTime=request.args.get("end_time")
      db.session.commit()
    return redirect('/therapist')

@app.route('/therapist/therapistInfo', methods=["GET", "POST"])
def therapistInfo():
    "Form to fill tharapist's information"
   
    form=TherapistAddForm()    
    
    if form.validate_on_submit():
         
            user=Therapist(therapistID=g.user.userID,first_name = form.first_name.data,
                         last_name = form.last_name.data,
                         phone = form.phone.data,
                         address = form.address.data,
                         speciality=form.speciality.data)
            db.session.add(user)
            db.session.commit()
            return render_template('/therapist/availability.html',user=user)
        
    return render_template('/therapist/therapistInfo.html',form=form)

@app.route('/therapist/showTherapist')
def show_therapist_inf():
       

    user = Therapist.query.filter_by(therapistID=g.user.userID).first_or_404()
    
  
    return render_template('/therapist/showTherapist.html', info=user.to_dict())

@app.route('/therapist/editTherapist',methods=["GET","POST"])
def edit_therapist():
    """Show therapist information and """
    user = Therapist.query.filter_by(therapistID=g.user.userID).first_or_404()
    form=TherapistAddForm(obj=user)

    if form.validate_on_submit():
         
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.phone = form.phone.data
            user.address = form.address.data
            
            db.session.commit()
            return render_template('/therapist/availability.html',user=user)
         
    return render_template('/therapist/editTherapist.html',form=form)


@app.route("/therapist/patientList")
def listPatients():
       patients = Patient.query.all()     
       return render_template("/therapist/listPatients.html",patient=patients)
    
@app.route("/therapist/appoint/<int:pat_ID>")
def therapAppoint(pat_ID):
    try:
      patientA = Schedule.query.filter_by(patientID=pat_ID).first_or_404()
      return render_template("/therapist/appoint.html",appoint=patientA)
    except:
      flash("No appointment in schedule.")
      return redirect("/therapist/patientList")   

@app.route("/therapist/statusAppointment/<int:patientID>",methods=["GET","PUT"])
def statusAppointment(patientID):  
    patient=Schedule.query.filter_by(patientID=patientID).first_or_404()
    patient.status=request.args.get("appoint_status")
    db.session.commit()
    return redirect("therapist/patientList")

@app.route("/therapist/patientInf/<int:pat_ID>")
def patientInf(pat_ID):
    user = Patient.query.filter_by(patientID=pat_ID).first_or_404()
    return render_template("/therapist/patientInf.html",info=user.to_dict())


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
    