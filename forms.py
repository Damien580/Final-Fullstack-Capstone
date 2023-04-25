from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Regexp

class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=255)])
    password = StringField('Password', validators=[DataRequired(), Length(min=8, max=24), Regexp(r'^.*(?=.{8,24})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=3*[@#$%^&+=]).*$', message='Password must be 8-24 characters, contain one number, one uppercase letter, and 3 special characters!')])
    user_bio = TextAreaField('Bio', validators=[Length(min=25, max=3000)])
    user_email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Create')

class AddPhoto(FlaskForm):
    url = StringField('Picture Address', validators=[DataRequired()])
    comment = TextAreaField('Comments')
    submit = SubmitField('Add')
    
    

    
