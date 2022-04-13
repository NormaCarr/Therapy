from models import Therapist, Patient
from datetime import datetime
import time
import json
import requests
from dateutil import parser

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

""" @app.route('/email') """
def emailvalid(email):
 
    url="https://emailvalidation.abstractapi.com/v1/?api_key=a49173e3e1714867be55051bfed4815f&email="
    url=url+email
    response = requests.get(url,stream=True)
    dictdata = json.loads(response.content)
    emailvar =dictdata["deliverability"]
    return emailvar
