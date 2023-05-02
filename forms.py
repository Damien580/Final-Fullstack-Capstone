from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, HiddenField, PasswordField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields import RadioField
from datetime import datetime
from model import User

class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    remember_me = BooleanField("remember me")
    submit = SubmitField("submit")

class NewUserForm(FlaskForm):
    new_username = StringField('Username', validators=[DataRequired(), Length(min=4, max=255)])
    new_password = StringField('Password', validators=[DataRequired(), Length(min=8, max=24)])
    user_bio = TextAreaField('Bio', validators=[Length(min=25, max=3000)])
    user_email = StringField('Email', validators=[DataRequired()])
    is_female = RadioField('Gender', choices=[('true', 'Female'), ('false', 'Male')], validators=[DataRequired()])
    submit = SubmitField('Create')
    

class AddPhotoForm(FlaskForm):
    url = StringField('Picture Address', validators=[DataRequired()])
    comment = TextAreaField('Comments')
    user_id = HiddenField()  
    submit = SubmitField('Add')
    
class SearchForm(FlaskForm):
    is_female = RadioField('Gender', choices=[('True', 'Female'), ('False', 'Male')], validators=[DataRequired()])
    
class MessageForm(FlaskForm):
    recipient = SelectField('Recipient', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.recipient.choices = [(user.id, user.username) for user in User.query.all()]
    
    