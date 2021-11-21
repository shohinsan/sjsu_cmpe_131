from flask import redirect, url_for
from flask_login import UserMixin

from projectdir import database, login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('register'))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    data_created = database.Column(database.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.data_created.strftime("%d/%m/%Y, %H:%M:%S")}'
