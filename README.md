
##Therapist

To get this application running, make sure you do the following in the Terminal:

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `createdb therapist`
5. `flask run`


------------- Routes

app.route('/')  
    ('/base.html')

/login', methods=["GET","POST"]

/logout



--------------- Thetapist

/therapist/therapistHome.html

/therapist/signup',methods=["GET","POST"]

/therapist/availability',methods=["GET","POST"]

/therapist/therapistInfo/<int:user_id>',methods=["GET","POST"]

/therapist/showTherapist/<int:user_id>

/therapist/editTherapist/<int:user_id>',methods=["GET","POST"]

/therapist/patientList

/therapist/appoint/<int:patient_id>

/therapist/patientInf/<int:patient_id>



--------------  Patient

/patient/patientHome.html

/patient/signup',methods=["GET","POST"]

/patient/patientInfo/<int:user_id>',methods=["GET","POST"]

/patient/editPatient/<int:user_id>',methods=["GET","POST"]

/patient/showPatient<int:user_id>



---------------- Shedule

/patient/appoint

/patient/editAppoint

/patient/cancelAppoint

/patient/appointment',methods=["GET","POST"]



--------------- Payment

/patient/account

/patient/listPayments

/patient/payment', methods=["GET","POST"]
