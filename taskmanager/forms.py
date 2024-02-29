from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, ValidationError, SelectField, DateField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from taskmanager.models import User



class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', 
                           validators=[DataRequired(), Length(min=3, max=50)])
    last_name = StringField('Last Name', 
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', 
                           validators=[DataRequired(), Email()])
    password = StringField('Password', 
                           validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', 
                           validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists!')
        

class LoginForm(FlaskForm):
    email = StringField('Email', 
                           validators=[DataRequired(), Email()])
    password = StringField('Password', 
                           validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')], validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    created_date = DateTimeField('Created Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[DataRequired()])
    submit = SubmitField('Create Task')

