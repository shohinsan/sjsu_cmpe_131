from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
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


class AccountUpdateForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    picture = FileField(label="Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Update Account')
    delete = SubmitField(label='Delete Account')


class DeleteAccountForm(FlaskForm):
    delete = SubmitField(label='Delete Account')


class PomodoroAndBlockForm(FlaskForm):
    study = IntegerField(label='Study', validators=[DataRequired()])
    rest = IntegerField(label='Rest', validators=[DataRequired()])
    blocks = IntegerField(label='Blocks', validators=[DataRequired()])
    submit = SubmitField(label="Start")


class NewFlashCard(FlaskForm):
    front = StringField('Frontside', validators=[DataRequired()])
    back = StringField('Backside', validators=[DataRequired()])
    submit = SubmitField('Add')


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add')


class ShareForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label="Submit")
