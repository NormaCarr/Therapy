##Therapist

To get this application running, make sure you do the following in the Terminal:

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `createdb therapist` or run python therapist_seed.py
5. `flask run`

This website will provide a friendly interface for managing therapies schedule and therapies fees payments.
The app will manage a therapist's schedule and client's bill. The therapist has to set his availability days and hours. The client has to login or create an account to see the therapist’s schedule and select a time. Also, he needs to provide payment information with a credit or debit card. 
The application has a database with five tables. 
-- One table with the therapist’s name, specialty, contact information, and office address. 
-- A table with the patient personal information, First name, last name,phone number, address.
-- Another table with payment information like patient id, amount, date, concept, and card. 
-- Another table with the patient schedule information, therapist id, patient id, day, time, frequency, status, and comment.
-- Another table with the user’s login information, user id, username(email), and password.



Routes

app.route('/')  
    ('/base.html')

/login', methods=["GET","POST"]
/logout


Thetapist

/therapist/therapistHome.html
/therapist/signup',methods=["GET","POST"]
/therapist/availability',methods=["GET","POST"]
/therapist/therapistInfo',methods=["GET","POST"]
/therapist/showTherapist
/therapist/editTherapist',methods=["GET","POST"]
/therapist/patientList
/therapist/appoint/<int:patient_id>
/therapist/patientInf/<int:patient_id>


Patient

/patient/patientHome.html
/patient/signup',methods=["GET","POST"]
/patient/patientInfo',methods=["GET","POST"]
/patient/editPatient',methods=["GET","POST"]
/patient/showPatient
/patient/editPatient',methods=["GET","POST"]


Shedule

/patient/appoint
/patient/new_appointment',methods=["POST"]
/patient/editAppoint
/patient/cancelAppoint',methods=["GET"]
/patient/appointment',methods=["GET","POST"]
/patient/modify_appointment', methods=["POST"]


Payment

/patient/account
/patient/listPayments
/patient/payment', methods=["GET","POST"]


Files

- app.py is the main function, it contains the roots decorators, and api calls 
- requirements.txt has all the libraris tha the app nedds to run.

- models.py has the database tables.

- forms.py contains the forms for the templates data enter and manipulation.

- utility_functon.py has all the utility functions that help the aplication to work.

- therapist_seed.py contains the necesary data to prefill the database tables to check the app funtionality.