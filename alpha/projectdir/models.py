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

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.data_created.strftime("%d/%m/%Y, %H:%M:%S")}'
