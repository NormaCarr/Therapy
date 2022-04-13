

from flask_wtf import FlaskForm
from wtforms import StringField,DateField,FloatField,SelectField,validators, PasswordField, TextAreaField
from wtforms.validators import EqualTo,DataRequired,ValidationError, Email, Length


class UserAddForm(FlaskForm):
    """Form for users information"""
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    phone = StringField('Phone',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])

class TherapistAddForm(FlaskForm):
    """Form for therapist information."""
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    phone = StringField('Phone',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()]) 


class PatientAddForm(FlaskForm):
    """Form for adding patient."""

    first_name = StringField("First_name", validators=[DataRequired()])
    last_name = StringField("Last_name", validators=[DataRequired()])
    phone = StringField("Phone",validators=[DataRequired()])
    address = StringField("Address",validators=[DataRequired()])
    
    
class SignupAddForm(FlaskForm):
    username = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=8)],)
    #password = PasswordField("Password",validators=[Length(min=4),DataRequired(message="Please enter a password."),])
    #confirmPassword = PasswordField ("Repeat Password",[EqualTo(password, message='Passwords must match.')])

class LoginForm(FlaskForm):
    username = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=4)],)

class PaymentForm(FlaskForm):
     amount = FloatField('Amount')
     concept = TextAreaField('Concept',validators=[DataRequired()])                  
     card = StringField('Card',validators=[Length(min=16),DataRequired()])
     expiration=StringField('exp',validators=[Length(min=5,max=5,message="MM/YY"),DataRequired()])
     CVV=StringField('CVV',validators=[Length(min=3,max=3,message="CVV"),DataRequired()])
     ZIP=StringField('ZIP',validators=[Length(min=5,max=5,message="ZIP"),DataRequired()])

