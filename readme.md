# Therapy

-[TherapistGroup link:](https://therapistt.herokuapp.com/)

##To get this application running, make sure you do the following in the Terminal:

-Get the api_key for [email validation](https://www.abstractapi.com/email-verification-validation-api) to place in the function emailvalid(email)

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`  
4. `createdb therapist` or run python therapist_seed.py
5. `flask run`

## **Description **

This website will provide a friendly interface for managing therapies schedule and therapies fees payments.
The app will manage a therapist's schedule and client's bill. The therapist has to set his availability days and hours. The client has to login or create an account to see the therapist’s schedule and select a time. Also, he needs to provide payment information with a credit or debit card. 
The application has a database with five tables. 
- One table with the therapist’s name, specialty, contact information, and office address. 
- A table with the patient personal information, First name, last name,phone number, address.
- Another table with payment information like patient id, amount, date, concept, and card. 
- Another table with the patient schedule information, therapist id, patient id, day, time, frequency, status, and comment.
- Another table with the user’s login information, user id, username(email), and password.

## ** Routes  **

> - app.route('/')  
    ('/base.html')

> - /login', methods=["GET","POST"]
> - /logout


> ### Thetapist

> > - /therapist/therapistHome.html
> > - /therapist/showTherapist
> > - /therapist/patientList
> > - /therapist/appoint/<int:patient_id>
> > - /therapist/patientInf/<int:patient_id>
> > - /therapist/signup',methods=["GET","POST"]
> > - /therapist/availability',methods=["GET","POST"]
> > - /therapist/therapistInfo',methods=["GET","POST"]
> > - /therapist/editTherapist',methods=["GET","POST"]




> ### Patient 

> > - /patient/patientHome.html
> > - /patient/showPatient
>> - /patient/signup',methods=["GET","POST"]
>> - /patient/patientInfo',methods=["GET","POST"]
>> - /patient/editPatient',methods=["GET","POST"]
>> - /patient/editPatient',methods=["GET","POST"]


> ### Shedule

>> - /patient/appoint
>> - /patient/editAppoint
>> - /patient/new_appointment',methods=["POST"]
>> - /patient/cancelAppoint',methods=["GET"]
>> - /patient/appointment',methods=["GET","POST"]
>> - /patient/modify_appointment', methods=["POST"]


> ### Payment

>> - /patient/account
>> - /patient/listPayments
>> - /patient/payment', methods=["GET","POST"]


##  ** Files ** 

- app.py is the main function, it contains the roots decorators, and python extensions calls 
- requirements.txt has all the libraries that the app needs to run.
- models.py has the database tables.
- forms.py contains the forms for the templates data entry and manipulation.
- utility_functons.py has all the utility functions that help the aplication to work.
  - IMPORTANT - The function def emailvalid(email): requires an api_key to validate the email when a user is creating an account. If you don't have it, the user won't be able to create an account.

- therapist_seed.py contains the necessary data to prefill the database tables to check the app functionality.
