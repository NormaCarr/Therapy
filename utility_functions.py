from models import Therapist, Patient,Schedule,User,db
from datetime import datetime
import time
import json
import requests
from dateutil import parser

def fill_database():
    u1=User.signup(username="petterParker@gmail.com",password="wonderfull")
    u2=User.signup(username="tinkerBell@hotmail.com",password="wonderfull")
    u3=User.signup(username="caspianGarcia@yahoo.com",password="wonderfull")
    u4=User.signup(username="wendyFriend@therapistGroup.com",password="therapistall")

    db.session.commit()

    p1 = Patient(patientID=1,first_name="Petter",last_name="Parker",address="315 W Foster Ave, Pampa, TX 79065",phone="+18066691473")
    p2 = Patient(patientID=2,first_name="Tinker",last_name="Bell",address="5320 S Rainbow Blvd #300, Las Vegas, NV 89118",phone="+17028929696")
    p3 = Patient(patientID=3,first_name="caspian",last_name="Garcia",address="2937 Palm Beach Blvd, Fort Myers, FL 33916",phone="+12395617427")
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.commit()

    t1 = Therapist(therapistID=4,first_name="Wendy",last_name="Darling",address="1260 6th Ave, New York, NY 10020",phone="+12124656741",speciality="Psycology",startDay="Monday",endDay="Saturday",startTime="09:00",endTime="15:00")
    db.session.add(t1)
    db.session.commit()

    sh1=Schedule(patientID=1,therapistID=4,day="2022-04-7",time="2:00",frequency="every_2weeks",status="to_comfirm",comments="None")
    sh2=Schedule(patientID=2,therapistID=4,day="2022-04-5",time="11:00",frequency="every_week",status="done",comments="We see the patient about 3 weeks after the rape in a community nursing home, where she was moved after a 4 day stay at the hospital.  She was very distressed, delusional and confused.  She slowly improved over 2 months and was discharged to a senior living building in a community in eastern Baltimore County. ")
    db.session.add(sh1)
    db.session.add(sh2)
    db.session.commit()

dayweek=('Monday','Tusday','Wednesday','Thursday','Friday','Saturday','Sunday')

def verifyAccount(user):
    """Verify is the account is from a patient or therapist"""
    if Therapist.query.get(user):
      return "therapist"
    else:
      if Patient.query.get(user):
         return "patient"
      else:
        return "None"
   
def validateStartTime(startT,endT):
    """Validate the start time is not after the end time"""
    if((startT>endT) or (startT==endT) or (startT=="") or endT==""):
        return 0
    return 1   

def currentDatetoArray():
    date=datetime.now()
    value=str(date.year)+'-'+str(date.month)+'-'+str(date.day)
    minim=str(date.year)+'-'+str(date.month)+'-'+str(date.day+2)
    maxim=str(date.year)+'-'+str(date.month+2)+'-'+str(date.day)
   
    return [value,minim,maxim]

def hideCardNumber(card):
    cardN = list(card)
    cardN[0:11]=['*','*','*','*','*','*','*','*','*','*','*','*']
    cardH=''.join(str(e) for e in cardN)
    return cardH
    

def validAppDayTime(data,therapApp):
    """Validate the appointment time and the therapist time"""
    
    if data:
        
        day= time.strptime(data[0], '%Y-%m-%d') #day has te time structur_time(tm_year,tm_mon,tm_mday,...tm_wday)
        wday=day.tm_wday
        startDay=therapApp.startDay
        endDay=therapApp.endDay
        startDay=dayweek.index(startDay)
        endDay=dayweek.index(endDay)
        if(startDay<=wday and wday<=endDay):
            if(therapApp.startTime<=data[1] and therapApp.endTime>=data[1]):
               return True
    return False


def emailvalid(email,api_key):
    """Get the user_api_key_value at https://www.abstractapi.com/email-verification-validation-api"""
    """ url="https://emailvalidation.abstractapi.com/v1/?api_key=user_api_key_value&email=" """
    
    url="https://emailvalidation.abstractapi.com/v1/?api_key=a49173e3e1714867be55051bfed4815f&email="
    url=url+email
    response = requests.get(url,stream=True)
    dictdata = json.loads(response.content)
    emailvar =dictdata["deliverability"]
    return emailvar
