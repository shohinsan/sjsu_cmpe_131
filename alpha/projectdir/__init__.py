from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

UPLOAD_FOLDER = 'sjsu_cmpe_131/alpha/projectdir/uploads'

app.config['UPLOADS'] = UPLOAD_FOLDER 
app.config['SECRET_KEY'] = 'groupnineproject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/notetaking.db'

app.config['TEMPLATES_AUTO_RELOAD'] = True

database = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

# Turn on "Less secure app access" from your google account
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# It's actually real gmail account
app.config['MAIL_USERNAME'] = 'teststringuser1@gmail.com'
app.config['MAIL_PASSWORD'] = 'Stringuser1'

mail = Mail(app)

# remove if necessary
app.config['MAX_CONTENT_LENGTH'] = 200 * 200


@app.before_first_request
def create_tables():
    database.create_all()


from projectdir import routes, models, forms
