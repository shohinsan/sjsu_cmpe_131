from flask import render_template, url_for, redirect, flash

from projectdir import app, database, bcrypt
from projectdir.forms import RegistrationForm, LoginForm
from projectdir.models import User


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/account')
def account():
    return render_template('account.html', title='About')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            flash(f'Login successful for {form.email.data}', category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Login unsuccessful for {form.email.data}', category='danger')
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
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
    # visuale blocks
    return render_template('time.html', title='Time Share')


@app.route('/calendar')
def calendar():
    # track assignments
    return render_template('calendar.html', title='Calendar')
