from datetime import datetime
import json

from flask import render_template, url_for, redirect, flash, request, session
from alpha.projectdir.forms import NotesForm
from alpha.projectdir.models import Notes

from projectdir import app, database, bcrypt, mail
from projectdir.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPasswordForm, AccountUpdateForm, DeleteAccountForm, TimerForm, NotesForm
from projectdir.models import User, TimerDetails # Quiz, Card
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import os


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


# Login/ Signup Features Starts

def save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_image(form.picture.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        database.session.commit()
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_url = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='About', legend="Account Details", form=form, image_url=image_url)


@app.route('/account/delete')
@login_required
def delete_account():
    form = AccountUpdateForm()
    return render_template('account.html', form=form)


@app.route('/account/delete_successful')
@login_required
def delete_successful():
    user = current_user.id
    database.session.query(User).filter(User.id == user).delete(synchronize_session=False)
    logout_user()
    flash('Your account has been successfully deleted.', 'success')
    database.session.commit()
    return redirect(url_for('login'))



@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Login successful for {form.email.data}', category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Login unsuccessful for {form.email.data}', category='danger')
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=encrypted_password)
        database.session.add(user)
        database.session.commit()
        flash(f'Account created successfully for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)


# Login/ Signup Features Ends


    # November 26 Added

#
# @app.route('/flashcards')
# def show_card(question_sets=None):
#     # user var from loging
#     # have two different paths for creating and reading flashcards
#     # mind map
#     return render_template('flashcard.html',
#                            title='Flashcards',
#                            question_sets=question_sets)
#
#
# @app.route('/quiz-<int:quiz_id>')
# def quiz(quiz_id):
#     quiz: Quiz = Quiz(quiz_id)
#     card = quiz.get_card()
#     return render_template('flash_blueprint.html',
#                            question=card.question,
#                            answer=json.dumps(card.answer),
#                            name=quiz.name)
#
# class Quiz:
#     def __init__(self, quiz_id):
#         self.name = Quiz.query.get(quiz_id).name
#         self.cards = Card.query.filter_by(quiz=quiz_id).all()
#
#     def __repr__(self):
#         return '<Quiz object containing %d flashcards>' % len(self.cards)
#
#     def show_all(self):
#         for c in self.cards:
#             print
#             c
#
#     def get_card(self):
#         return random.choice(self.cards)
# November 26 Added


@app.route('/md_notes')
@login_required
def md_notes():
    form = NotesForm()

    return render_template('mdnotes.html', title='Markdown', form=form)


@app.route('/finder')
def finder():
    # rename and find files 
    return render_template('find.html', title='Finder')


@app.route('/timer', methods=['GET', 'POST'])
@login_required
def time():
    form=TimerForm()
    return render_template('timer.html', title='Timer', form=form)

@app.route('/countdown')
def count():
    print(datetime.now())
    session['starttime']=datetime.now()
    return render_template('timeractual.html', Timer=25)


#database for some reason doesn't exit 
@app.route('/break')
def shortbreak():
    print(datetime.now())
    session['endtime']=datetime.now()
    timespent=session['endtime']-session['starttime']
    timer = TimerDetails(id=datetime.now().day, time=timespent.total_seconds()//60)
    # database.session.add(timer)
    # database.session.commit()
    return render_template('break.html', Break=5)
def longbreak():
    print(datetime.now())
    session['endtime']=datetime.now()
    timespent=session['endtime']-session['starttime']
    timer = TimerDetails(id=datetime.now().day, time=timespent.total_seconds()//60)
    # database.session.add(timer)
    # database.session.commit()
    return render_template('break.html', Break=15)


# Forgot Password Feature Starts


def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@scholarrabbit.com')
    msg.body = f''' To reset your password. Please follow the link below
    
    {url_for('reset_token', token=token, _external=True)}
    
    If you didn't send a password reset request. Please ignore this message.
    
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash('Reset request sent. Check your mail', 'success')
            return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Request", form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash('That is invalid token or expired. Please try again.', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        database.session.commit()
        flash('Password changed! Please login!', 'success')
        return redirect(url_for('login'))
    return render_template('change_password.html', title="Change Password", legend="Change Password", form=form)


# Forgot Password Feature Ends


@app.route('/calendar')
def calendar():
    # track assignments
    return render_template('calendar.html', title='Calendar')
