from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, RadioField, TextAreaField, FileField
from wtforms.validators import InputRequired

class ProfileForm(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired()]) 
    lastname = StringField('Lastname', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    gender = RadioField('Gender',choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    image = FileField('Profile Pic')