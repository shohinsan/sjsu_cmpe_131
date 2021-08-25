from projectdir import app
from flask import render_template


@app.route('/')
@app.route('/home')
def homepage():  # put application's code here
    return render_template("homepage.html")
