from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm = PasswordField('Confirm Password', validators=[EqualTo('password')])
    role = SelectField('Role', choices=[('jobseeker','Jobseeker'),('employer','Employer')], validators=[DataRequired()])
    company = StringField('Company (if Employer)')
    submit = SubmitField('Register')

class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location')
    submit = SubmitField('Post Job')

class ApplyForm(FlaskForm):
    cover_letter = TextAreaField('Cover Letter', validators=[Length(max=2000)])
    submit = SubmitField('Apply')
