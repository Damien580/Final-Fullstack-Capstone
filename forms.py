from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import RadioField

class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    remember_me = BooleanField("remember me")
    submit = SubmitField("submit")

class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=255)])
    password = StringField('Password', validators=[DataRequired(), Length(min=8, max=24)])
    user_bio = TextAreaField('Bio', validators=[Length(min=25, max=3000)])
    user_email = StringField('Email', validators=[DataRequired()])
    is_female = RadioField('Gender', choices=[('true', 'Female'), ('false', 'Male')], validators=[DataRequired()])
    submit = SubmitField('Create')

class AddPhotoForm(FlaskForm):
    url = StringField('Picture Address', validators=[DataRequired()])
    comment = TextAreaField('Comments')
    user_id = HiddenField(validators=[DataRequired()])  
    submit = SubmitField('Add')
    
class SearchForm(FlaskForm):
    is_female = RadioField('Gender', choices=[('True', 'Female'), ('False', 'Male')], validators=[DataRequired()])