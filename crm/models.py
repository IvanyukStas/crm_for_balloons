from crm import db
from datetime import datetime

class Client(db.Model):
    """
    Таблица клиента
    """
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, index=True)
    client_phone = db.Column(db.Integer, index=True, unique=True)
    client_birthday = db.Column(db.String, index=True)
    client_registration = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    client_family = db.relationship('ClientFamily', backref='client', lazy='dynamic')

    def __repr__(self):
        return f'<Клиент: {self.client_name}>'


class ClientFamily(db.Model):
    """
    Таблица родственников клиента
    """
    id = db.Column(db.Integer, primary_key=True)
    client_family_name = db.Column(db.String, index=True)
    client_family_phone = db.Column(db.Integer, index=True, unique=True)
    client_family_birthday = db.Column(db.String, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))


    def __repr__(self):
        return f'<Семья клиента: {self.client_family_name}>'