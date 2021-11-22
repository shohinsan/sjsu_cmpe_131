from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label='Sign Up')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField(label='Login')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired()])

    submit = SubmitField(label='Change Password', validators=[DataRequired()])


class ResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])

# class PomodoroForm(FlaskForm):
#     email = StringField(label='Email', validators=[DataRequired(), Email()])
#     password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField(label='Login')
