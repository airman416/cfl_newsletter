from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class PostForm(FlaskForm):
    title = TextAreaField('Title', validators=[
        DataRequired(), Length(min=1, max=30)])
    summary = TextAreaField('Summary', validators=[
        DataRequired(), Length(min=1, max=100)])
    post = TextAreaField('Content', validators=[
        DataRequired(), Length(min=1, max=1000)])
    topic = StringField('Topic', validators=[
        DataRequired(), Length(min=1, max=30)])
    submit = SubmitField('Submit')