from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for users information"""
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Phone',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])

class TherapistAddForm(FlaskForm):
    """Form for therapist information."""
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Phone',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()]) 


class PatientAddForm(FlaskForm):
    """Form for adding patient."""

    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('Phone',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    
    
class SignupAddForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=4)])
    

