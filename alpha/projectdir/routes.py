from flask import render_template, url_for, redirect, flash, request, session
from projectdir import app, database, bcrypt, mail
from projectdir.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPasswordForm
from projectdir.models import User
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='About')


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


@app.route('/flashcards')
def flashcards():
    # user var from loging
    # have two different paths for creating and reading flashcards
    # mind map
    return render_template('flashcards.html', title='Flashcards')


@app.route('/md_notes')
def md_notes():
    # render notes 
    # print notes to pdf
    # share notes
    # notes tree 
    return render_template('mdnotes.html', title='Markdown')


@app.route('/finder')
def finder():
    # rename and find files 
    return render_template('find.html', title='Finder')


@app.route('/time')
def time():
    # create Blocks
    # visualize blocks
    return render_template('time.html', title='Time Share')


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


#
# @app.route('/pomodoro', methods=["GET", "POST"])
# @login_required
# def pomodoro():
#     session['login'] = False
#     if request.method == 'POST':
#         inputTimerTarget = request.form['pomodoroInterval']
#         inputBreakTarget = request.form['breakInterval']
#
#         # convert times to minutes:
#         timerTarget = inputTimerTarget[3:]
#         breakTarget = inputBreakTarget[3:]
#
#         # save timer intervals for logged in user
#         newTimerDetails = TimerDetails(pomodoro_interval=timerTarget,
#                                        break_interval=breakTarget)
#         database.session.add(newTimerDetails)
#         database.session.commit()
#
#     else:
#         timerDetails = TimerDetails.query.filter_by(username=current_user.username).first()
#         if (timerDetails):
#             inputTimerTarget = ('00:' + str(timerDetails.pomodoro_interval))
#             inputBreakTarget = ('00:' + str(timerDetails.break_interval))
#             return render_template('pomodoro.html', timerTarget=timerDetails.pomodoro_interval,
#                                    breakTarget=timerDetails.break_interval,
#                                    inputTimerTarget=inputTimerTarget,
#                                    inputBreakTarget=inputBreakTarget)
#         else:
#             timerTarget = '25'
#             breakTarget = '5'
#             return render_template('pomodoro.html', timerTarget=timerTarget, breakTarget=breakTarget,
#                                    inputTimerTarget=timerTarget, inputBreakTarget=breakTarget)


@app.route('/calendar')
def calendar():
    # track assignments
    return render_template('calendar.html', title='Calendar')
