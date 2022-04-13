
from unittest import TestCase
from urllib import response
from flask import session
from models import db
from app import app
from utility_functions import validAppDayTime,verifyAccount,validateStartTime

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:metal@localhost:5432/therapist'
app.config['SQLALCHEMY_ECHO'] = False
# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

therapApp = {'startDay':'Monday','endDay':'Friday','startTme':'11:00','endTime':'16:00'}
valDataApp=['2022-04-24','10:00']
valDataApp2=['2022-04-24','10:']

class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True 
        
    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""
        with self.client:
            response = self.client.get('/')
            self.assertIn(b'Therapist',response.data)
            self.assertIn(b'Patient',response.data)

    def test_patient(self):
        """Make sure information is in the session and HTML is displayed"""
        with self.client:
            response = self.client.get('/patient')
            self.assertIn(b'Create account',response.data)
            self.assertIn(b'Log in',response.data)

    def test_therapist(self):
        """Make sure information is in the session and HTML is displayed"""
        with self.client:
            response = self.client.get('/therapist') 
            self.assertIn(b'Log in',response.data)
    
    def test_login(self):
        """Make sure information is in the session and HTML is displayed"""
        with self.client:
            response = self.client.get('/login')
            self.assertIn(b'name="username"',response.data)
            self.assertIn(b'password',response.data)

    def test_appointment(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:
            response = client.get('/patient/appoint')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'name="day"',response.data)
    
    
    def test_account(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:
            response = client.get('/patient/account')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'href="/patient/payment"',response.data)
            self.assertIn(b'href="/patient/listPayments"',response.data)
            self.assertIn(b'href="/patient"',response.data)
     
    def test_payment(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:
            response = client.get('/patient/payment')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'href="/patient"',response.data)


    def test_show_list_payment(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:       
            url='/patient/listPayment'
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'href="/patient"',response.data)

    def test_edit_patient_inf(self):
        """Make sure information is in the session and HTML is displayed"""
        
        with app.test_client() as client:   
            response = client.get('/patient/editPatient')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'id="patient_form"',response.data)
            
            
         
    def test_calendar(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:
            response = client.get('/calendar')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'href="/therapist"',response.data)

    def test_show_patient_inf(self):
        """Make sure information is in the session and HTML is displayed"""
       
        with app.test_client() as client:       
            url='/patient/showPatient'
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'href="/patient"',response.data)
    

    def test_validAppDayTime(self):
        self.assertTrue(validAppDayTime(valDataApp,therapApp))
        self.assertFalse(validAppDayTime(valDataApp2,therapApp))
        self.assertFalse(validAppDayTime("",therapApp))

    def test_verifyAccount(self):
         self.assertEqual(verifyAccount(4),'therapist')
         self.assertEqual(verifyAccount(1),'patient')
         self.assertEqual(verifyAccount(0),'None')
    
    def test_validateStartTime(self):
        self.assertEqual(validateStartTime("12:00","07:00"),0)
        self.assertEqual(validateStartTime("02:00","07:00"),1)
        self.assertEqual(validateStartTime("04:00","04:00"),0)
        self.assertEqual(validateStartTime("",""),0)
        self.assertEqual(validateStartTime("02:00",""),0)
        self.assertEqual(validateStartTime("","07:00"),0)

    
    def test_show_list_patients(self):
        """Make sure information is in the session and HTML is displayed"""
        with app.test_client() as client:       
            url='/therapist/patientList'
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'href="/therapist"',response.data)       
        
    def test_show_therapist_inf(self):
        """Make sure information is in the session and HTML is displayed"""
       
        with app.test_client() as client:       
            url='/therapist/showTherapist'
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'href="/therapist/editTherapist"',response.data)
    
    def test_edit_therapist_inf(self):
        """Make sure information is in the session and HTML is displayed"""
      
        with app.test_client() as client:       
            url='/therapist/editTherapist'
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'id="therapistInfo_form',response.data)
        
    def test_fill_therapist_inf(self):
        """Make sure information is in the session and HTML is displayed"""
        
        with app.test_client() as client:       
            url='/therapist/therapistInfo'
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'id="therapistInfo_form',response.data)