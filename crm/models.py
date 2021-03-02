from crm import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    """
    Таблица зарегестрированных пользователей
    """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db. String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    clients = db.relationship('Client', backref='own_client', lazy='dynamic')

    def __repr__(self):
        return f"<User: {self.user}>"


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




class Client(db.Model):
    """
    Таблица добавленных клиентовклиента
    """
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, index=True)
    client_phone = db.Column(db.Integer, index=True, unique=True)
    client_birthday = db.Column(db.DateTime, index=True)
    client_registration = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_family = db.relationship('ClientFamily', backref='client', lazy='dynamic')


    def __repr__(self):
        return f'<Клиент: {self.client_name}>'


class ClientFamily(db.Model):
    """
    Таблица родственников клиента
    """
    id = db.Column(db.Integer, primary_key=True)
    client_family_name = db.Column(db.String, index=True)
    client_family_birthday = db.Column(db.String, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))


    def __repr__(self):
        return f'<Семья клиента: {self.client_family_name}>'