from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterFormPatient(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', choices=[('male','Male'),('female','Female'),('other','Other')], validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('patient', 'Patient')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), Length(min=1, max=3)])
    submit = SubmitField('Sign Up') 

class RegisterFormDoctor(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('doctor', 'Doctor')], validators=[DataRequired()])
    specialisation = StringField('Specialization', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role= SelectField('Role', choices=[('doctor', 'Doctor'), ('patient', 'Patient')], validators=[DataRequired()])
    submit = SubmitField('Login')


class AppointmentForm(FlaskForm):
    doctor = SelectField('Doctor', choices=[], coerce=int, validators=[DataRequired()])
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    date = StringField('Date: %Y-%m-%d', validators=[DataRequired()])
    time = StringField('Time: %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')




