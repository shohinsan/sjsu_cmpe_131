from projectdir import app
from flask import render_template


@app.route('/')
@app.route('/home')
def homepage():  # put application's code here
    return render_template("homepage.html", title='Home')

@app.route('/about')
def about():  # put application's code here
    return render_template("about.html", title='About')

@app.route('/account')
def account():  # put application's code here
    return render_template("account.html", title='About')

@app.route('/login')
def login():
    return render_template("login.html", form="login", title="Login")

@app.route('/signup')
def signup():
    return render_template("signup.html", form="signup", title="Registration")