import os

from flask import render_template, url_for, redirect, flash, request, session, send_file
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from fpdf import FPDF
from werkzeug.utils import send_file, secure_filename

from projectdir import app, database, bcrypt, mail
from projectdir.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPasswordForm, AccountUpdateForm, \
    NewFlashCard, NoteForm, ShareForm
from projectdir.models import User, Note, Flashcard, Events, TimerDetails

ALLOWED_EXTENSIONS = {'md'}
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)


# import markdown
# import markdown.extensions.fenced_code

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home')


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
    return render_template('general/account.html', title='About', legend="Account Details", form=form,
                           image_url=image_url)


@app.route('/account/delete')
@login_required
def delete_account():
    # A function helper to delete user from database (takes care of button)
    form = AccountUpdateForm()
    return render_template('general/account.html', form=form)


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
    return render_template('general/login.html', title='Login', form=form)


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
    return render_template('general/registration.html', title='Registration', form=form)


# Login/ Signup Features Ends


@app.route('/flashcards')
@login_required
def flashcards():
    # user var from loging
    # have two different paths for creating and reading flashcards
    # mind map
    user = User.query.filter_by(username=current_user.username).first()
    flashcards = Flashcard.query.filter_by(user_id=user.id).all()

    return render_template('flashcardz/flashcards.html', flashcards=flashcards, title='Flashcards')


@app.route('/flashcards/<int:flashcard_id>')
@login_required
def show_flashcard(flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    return render_template('flashcardz/flashcard.html', flashcard=flashcard, title='Flashcard')


@app.route('/memorize')
@login_required
def memorize():
    user = User.query.filter_by(username=current_user.username).first()
    flashcards = Flashcard.query.filter_by(user_id=user.id).first()
    return render_template('flashcardz/memorize.html', flashcard=flashcards, title="Memorize")


@app.route("/flashcards/<int:flashcard_id>/update", methods=['GET', 'POST'])
@login_required
def update_flashcard(flashcard_id):
    # A function to update notes from database
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    if flashcard.author != current_user:
        os.abort(403)
    form = NewFlashCard()
    if form.validate_on_submit():
        flashcard.front = form.front.data
        flashcard.back = form.back.data
        database.session.commit()
        flash(f'Your flashcard has been updated successfully!', 'success')
        return redirect(url_for('show_flashcard', flashcard_id=flashcard.id))
    elif request.method == 'GET':
        form.front.data = flashcard.front
        form.back.data = flashcard.back
    return render_template('flashcardz/createFlashcard.html', title='Update Flashcard', form=form,
                           legend='Update Flashcard')


@app.route("/flashcards/add", methods=['POST', 'GET'])
@login_required
def create_flashcard():
    form = NewFlashCard()
    if form.validate_on_submit():
        flashcard = Flashcard(front=form.front.data, back=form.back.data, user_id=current_user.id)
        database.session.add(flashcard)
        database.session.commit()
        flash(f'Successfully added new Flashcard!', 'success')
        return redirect('/flashcards')
    return render_template('flashcardz/createFlashcard.html', form=form, title='Create Flashcard')


@app.route("/flashcards/<int:flashcard_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_flashcard(flashcard_id):
    # A function to delete notes from database
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    if flashcard.author != current_user:
        os.abort(403)
    database.session.delete(flashcard)
    database.session.commit()
    flash(f'Your flashcard has been deleted successfully!', 'success')
    return redirect(url_for('flashcards'))


@app.route("/flashcards/<int:flashcard_id>/share", methods=['GET', 'POST'])
@login_required
def share_flashcard(flashcard_id):
    # A function helper to share notes with other users in database
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    form = ShareForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_user(form.username.data):
            flash(f'Invalided Account! This account does not exist!')
            return redirect(url_for('share_flashcard', flashcard_id=flashcard.id))
        newFlashcard = Flashcard(front=flashcard.front, back=flashcard.back, user_id=user.id)
        database.session.add(newFlashcard)
        database.session.commit()
        flash(f'Successfully Shared Flashcard!', 'success')
        return redirect(url_for('show_flashcard', flashcard_id=flashcard.id))
    return render_template('notes/shareNote.html', form=form, title='Share Flashcard')


@app.route('/flashcards/<int:flashcard_id>/pdf', methods=['GET', 'POST'])
@login_required
def flashcard_pdf(flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=14)
    pdf.multi_cell(w=40, h=20, txt=flashcard.front + '\n' + flashcard.back, align='C')
    pdf.output('output_flashcard.pdf')
    return send_file('output_flashcard.pdf', as_attachment=True, environ=request.environ)


@app.route("/flashcards/addfile", methods=['POST', 'GET'])
@login_required
def add_flashcard():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(uploads_dir, filename))
            f = open(os.path.join(uploads_dir, filename), 'r')
            flashcardfront = filename.split('.md', 1)[0]
            flashcardback = ''
            # Only adds front if there is a header in the md file; accepts the format
            ''' 
            # Title 
            Content below the title 
            '''
            for x in f:
                if x[0] == '#':
                    flashcardfront = x[1:len(x) - 1]
                else:
                    flashcardback += x
            flashcard = Flashcard(front=flashcardfront, back=flashcardback, user_id=current_user.id)
            database.session.add(flashcard)
            database.session.commit()
            flash('Succesfully added flashcard to database', 'success')
            return redirect(url_for('flashcards'))
    return render_template('flashcardz/createMDFlashcard.html', title='Markdown to Flashcard')


# Flashcard End


@app.route('/notes')
@login_required
def notes():
    # A function to display all the notes
    user = User.query.filter_by(username=current_user.username).first()
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('notes/notes.html', notes=notes, title='Notes')


@app.route('/search')
@login_required
def n_search():
    q = request.args.get('q')
    if q:
        notes = Note.query.filter(Note.title.contains(q) | Note.content.contains(q))
    else:
        notes = Note.query.all()
    return render_template('notes/searched_notes.html', notes=notes, title='Notes')


@app.route('/search_flash')
@login_required
def f_search():
    q = request.args.get('q')
    if q:
        flashcards = Flashcard.query.filter(Flashcard.front.contains(q) | Flashcard.back.contains(q))
    else:
        flashcards = Flashcard.query.all()
    return render_template('flashcardz/searched_flashcards.html', flashcards=flashcards, title='Flashcards')


@app.route('/notes/<int:note_id>')
@login_required
# A function to click each note and get to another route
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('notes/note.html', note=note, title=note.title)


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
    return render_template('notes/createNote.html', form=form, title='Add Notes')


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/notes/upload', methods=['GET', 'POST'])
@login_required
def upload_note():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(uploads_dir, filename))
            f = open(os.path.join(uploads_dir, filename), 'r')
            notetitle = filename.split('.md', 1)[0]
            notecontent = ''
            # Only adds title if there is a header in the md file 
            for x in f:
                if x[0] == '#':
                    notetitle = x[1:]
                else:
                    notecontent += x
            note = Note(title=notetitle, content=notecontent, user_id=current_user.id)
            database.session.add(note)
            database.session.commit()
            flash('Succesfully added note to database')
            return redirect(url_for('notes'))
    return render_template('notes/uploadnote.html', title='Upload a Markdown file')


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
        flash(f'Your note has been updated successfully!', 'success')
        return redirect(url_for('note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('notes/createNote.html', title='Update Note', form=form, legend='Update Note')


@app.route("/notes/<int:note_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    # A function to delete notes from database
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        os.abort(403)
    database.session.delete(note)
    database.session.commit()
    flash(f'Your note has been deleted successfully!', 'success')
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
        flash(f'Successfully Shared Note!', 'success')
        return redirect(url_for('note', note_id=note.id))
    return render_template('notes/shareNote.html', form=form, title='Share Note')


@app.route('/notes/<int:note_id>/pdf', methods=['GET', 'POST'])
@login_required
def pdf(note_id):
    note = Note.query.get_or_404(note_id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=14)
    pdf.multi_cell(w=40, h=20, txt=note.title + '\n' + note.content, align='C')
    pdf.output('output_notes.pdf')
    return send_file('output_notes.pdf', as_attachment=True, environ=request.environ)


@app.route('/timer', methods=['GET', 'POST'])
@login_required
def time():
    if request.method == "POST":
        study = int(request.form["study"])
        rest = int(request.form["rest"])
        blocks = int(request.form["blocks"])

        session["study"] = study
        session["rest"] = rest
        session["blocks"] = blocks
        session["study_counter"] = 0

        return redirect(url_for("study"))
    return render_template('timing/timer.html', title='Timer')


@app.route('/rest')
@login_required
def rest():
    return render_template('timing/rest.html', title='Time To Rest', rest=session["rest"])


@app.route('/study')
@login_required
def study():
    if session["study_counter"] == session["blocks"]:
        return redirect(url_for("study_completed"))
    session["study_counter"] += 1
    return render_template('timing/study.html', title='Time To Study', study=session["study"])


@app.route('/completed-studying')
@login_required
def study_completed():
    user = User.query.filter_by(username=current_user.username).first()
    timeblock = TimerDetails(time=session['study_counter'] * session['study'], user_id=current_user.id)
    database.session.add(timeblock)
    database.session.commit()
    blocks = TimerDetails.query.filter_by(user_id=user.id).all()
    return render_template("timing/study_completed.html")


@app.route('/visualizeblocks')
@login_required
def visualize_blocks():
    user = User.query.filter_by(username=current_user.username).first()
    blocks = TimerDetails.query.filter_by(user_id=user.id).all()
    return render_template('timing/visualizeblocks.html', title='Timeblocks', blocks=blocks,
                           study_counter=session["study_counter"], study=session["study"])


# Timer End


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
    return render_template('general/reset_request.html', title="Reset Request", form=form)


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
    return render_template('general/change_password.html', title="Change Password", legend="Change Password", form=form)


# Forgot Password Feature Ends


@app.route('/calendar')
@login_required
def calendar():
    user = User.query.filter_by(username=current_user.username).first()
    events = Events.query.filter_by(user_id=user.id).all()
    # track assignments
    return render_template('timing/calendar.html', title='Calendar', events=events)


@app.route('/add_calendevent', methods=['GET', "POST"])
@login_required
# A function to add calendar events to database
def add_calendar_event():
    if request.method == "POST":
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']

        events = Events(title=title, start=start, end=end, url=url, user_id=current_user.id)
        database.session.add(events)
        database.session.commit()

        flash('Event added successfully', 'success')
        return redirect(url_for('calendar'))

    return render_template("timing/add_event.html", title='Calendar')
