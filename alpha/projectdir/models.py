from flask import redirect, url_for
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from projectdir import database, login_manager, app
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('registration'))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    # this must be date_created, but I misspelled and left it since it was messing my database
    # when changing the naming and it was lots of other workarounds
    data_created = database.Column(database.DateTime, default=datetime.utcnow())
    
    notes = database.relationship('Note', backref='author', lazy=True)


    
    def get_token(self, expires_sec=300):
        serial = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def check_user(sefl, username):
        if username != sefl.username:
            return False
        return True

    def __repr__(self):
        return f'{self.id} ' \
               f': {self.username} ' \
               f': {self.email} ' \
               f': {self.data_created.strftime("%d/%m/%Y, %H:%M:%S")}'

class TimerDetails(database.Model):
    id = database.Column(database.String(10), primary_key=True)
    time = database.Column(database.Integer)

    def __repr__(self):
        return f'{self.id}: {self.time}'


class Note(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(64), nullable=False)
    date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    content = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Note('{self.title}', '{self.date}')"

