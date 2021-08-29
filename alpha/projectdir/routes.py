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