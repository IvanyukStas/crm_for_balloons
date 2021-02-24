from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from crm.models import Client, ClientFamily

class CientForm(FlaskForm):
    '''
    Форма создания нвоого клиента
    '''
    client_name = StringField('Имя клиента')
    client_phone = IntegerField('Номер клиента с +7', validators=[DataRequired()])
    client_birthday = StringField('День рождения клиента')
    submit = SubmitField('Добавить')

    def validate_client_phone(self, client_phone):
        client = Client.query.filter_by(client_phone=client_phone.data).first()
        if client is not None:
            raise ValidationError("Такой телефон уже используется!!!")