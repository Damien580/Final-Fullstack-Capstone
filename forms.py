from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, HiddenField, PasswordField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields import RadioField

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")

class NewUserForm(FlaskForm):
    new_username = StringField('Username', validators=[DataRequired(), Length(min=4, max=255)])
    new_password = StringField('Password', validators=[DataRequired(), Length(min=8, max=24)])
    user_bio = TextAreaField('Bio', validators=[Length(min=25, max=3000)])
    user_email = StringField('Email', validators=[DataRequired()])
    is_female = RadioField('I am:', choices=[('true', 'Female'), ('false', 'Male')], validators=[DataRequired()])
    submit = SubmitField('Create')
    

class AddPhotoForm(FlaskForm):
    url = FileField('Picture Address', validators=[DataRequired()])
    comment = TextAreaField('Comments')
    user_id = HiddenField()  
    submit = SubmitField('Add')
    
class SearchForm(FlaskForm):
    is_female = RadioField('I am searching for a', choices=[('True', 'Female'), ('False', 'Male')], validators=[DataRequired()])
    submit = SubmitField('Search')
    
class MessageForm(FlaskForm):
    sender_id = HiddenField('Sender')
    recipient = SelectField('Recipient', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
