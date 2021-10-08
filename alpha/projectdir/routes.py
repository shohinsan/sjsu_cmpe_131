from projectdir import app
from flask import render_template, url_for, redirect, flash
from projectdir.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/home')
def homepage():  # put application's code here
    return render_template('homepage.html', title='Home')


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html', title='About')


@app.route('/account')
def account():  # put application's code here
    return render_template('account.html', title='About')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abd.shohin@gmail.com' and form.password.data == '123456':
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
        flash(f'Account created successfully for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)
