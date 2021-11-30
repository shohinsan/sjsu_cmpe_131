from datetime import datetime

from fpdf import FPDF
from flask import render_template, url_for, redirect, flash, request, session, make_response, send_file
from werkzeug.utils import send_file
from wtforms import widgets

from projectdir import app, database, bcrypt, mail
from projectdir.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPasswordForm, AccountUpdateForm, \
    NewFlashCard, NoteForm, ShareForm, TimerForm
from projectdir.models import User, Note, TimerDetails
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import os


# import markdown
# import markdown.extensions.fenced_code

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home')


@app.route('/about')
# non-functional method, will be removed by the 3rd milestone
def about():
    return render_template('about.html', title='About')


# Login/ Signup Features Starts

def save_image(picture_file):
    # A function to save image in project database
    picture_name = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # A function to update username, email, and profile picture max of (200x200) I set a limit
    # because it was huge at first
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
    # A function helper to delete user from database (takes care of button)
    form = AccountUpdateForm()
    return render_template('account.html', form=form)


@app.route('/account/delete_successful')
@login_required
def delete_successful():
    # A function to delete user from database
    user = current_user.id
    database.session.query(User).filter(User.id == user).delete(synchronize_session=False)
    logout_user()
    flash('Your account has been successfully deleted.', 'success')
    database.session.commit()
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    # A function to log in to system
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Login successful for {form.email.data}', category='success')
            return redirect(url_for('notes'))
        else:
            flash(f'Login unsuccessful for {form.email.data}', category='danger')
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    # A function to log out of system
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    # A function to register a user into database
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


@app.route('/flashcards')
def flashcards():
    # user var from loging
    # have two different paths for creating and reading flashcards
    # mind map
    """
    user = User.query.filter_by(username=current_user.username).first()
    cards = Flashcards.query.filter_by(user_id=user.id).all()
    form = NewFlashCard()
    if form.validate_on_submit():
        read_file = open(form.markdownFile.data,"r")
        content = markdown.markdown(read_file.read(), extensions=["fenced_code"])
        newCard = NewFlashCard(user_id=user.id, content=content)
        database.session.add(newCard)
        database.session.commit()
        flash(f'Upload Flashcard Successfully!')
        return redirect(url_for('flashcards'))
    """
    return render_template('flashcards.html', title='Flashcards')


@app.route('/notes')
@login_required
def notes():
    # A function to display all the notes
    user = User.query.filter_by(username=current_user.username).first()
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('notes.html', notes=notes, title='Notes')


@app.route('/notes/<int:note_id>')
@login_required
# A function to click each note and get to another route
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note=note, title=note.title)


@app.route('/notes/add', methods=['GET', 'POST'])
@login_required
# A function to add notes to database
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, user_id=current_user.id)
        database.session.add(note)
        database.session.commit()
        flash(f'Successfully added new note!', 'success')
        return redirect('/notes')
    return render_template('createNote.html', form=form, title='Add Notes')


@app.route("/note/<int:note_id>/update", methods=['GET', 'POST'])
@login_required
def update_note(note_id):
    # A function to update notes from database
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        os.abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        database.session.commit()
        flash(f'Your note has been updated successfully!')
        return redirect(url_for('note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('createNote.html', title='Update Note', form=form, legend='Update Note')


@app.route("/notes/<int:note_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    # A function to delete notes from database
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        os.abort(403)
    database.session.delete(note)
    database.session.commit()
    flash(f'Your note has been deleted successfully!')
    return redirect(url_for('notes'))


@app.route("/notes/<int:note_id>/share", methods=['GET', 'POST'])
@login_required
def share_note(note_id):
    # A function helper to share notes with other users in database
    note = Note.query.get_or_404(note_id)
    form = ShareForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_user(form.username.data):
            flash(f'Invalided Account! This account does not exist!')
            return redirect(url_for('share_note', note_id=note.id))
        newNote = Note(title=note.title, content=note.content, user_id=user.id)
        database.session.add(newNote)
        database.session.commit()
        flash(f'Successfully Shared Note!')
        return redirect(url_for('note', note_id=note.id))
    return render_template('shareNote.html', form=form, title='Share Note')

@app.route('/notes/<int:note_id>/pdf', methods=['GET', 'POST'])
@login_required
def pdf(note_id):
    note = Note.query.get_or_404(note_id)
    pdf=FPDF()
    pdf.add_page() 
    pdf.set_font('Arial', size=14)
    pdf.multi_cell(w=40, h=20, txt=note.title+'\n'+note.content, align='C')
    pdf.output('output.pdf')
    return send_file('output.pdf', as_attachment=True, environ=request.environ)

@app.route('/finder')
def finder():
    # rename and find files 
    return render_template('find.html', title='Finder')


@app.route('/timer', methods=['GET', 'POST'])
@login_required
def time():
    form = TimerForm()
    return render_template('timer.html', title='Timer', form=form)


@app.route('/countdown')
def count():
    print(datetime.now())
    session['starttime'] = datetime.now()
    return render_template('timeractual.html', Timer=25)


# database for some reason doesn't exit
@app.route('/break')
def shortbreak():
    print(datetime.now())
    session['endtime'] = datetime.now()
    timespent = session['endtime'] - session['starttime']
    timer = TimerDetails(id=datetime.now().day, time=timespent.total_seconds() // 60)
    # database.session.add(timer)
    # database.session.commit()
    return render_template('break.html', Break=5)


def longbreak():
    print(datetime.now())
    session['endtime'] = datetime.now()
    timespent = session['endtime'] - session['starttime']
    timer = TimerDetails(id=datetime.now().day, time=timespent.total_seconds() // 60)
    # database.session.add(timer)
    # database.session.commit()
    return render_template('break.html', Break=15)


# Forgot Password Feature Starts


def send_mail(user):
    # Send email confirmation to change password
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@scholarrabbit.com')
    msg.body = f''' To reset your password. Please follow the link below
    
    {url_for('reset_token', token=token, _external=True)}
    
    If you didn't send a password reset request. Please ignore this message.
    
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # A route to activate reset password button
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
    # Password change helper
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
