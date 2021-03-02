from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, BooleanField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from crm.models import Client, ClientFamily, User


class ClientForm(FlaskForm):
    '''
    Форма создания нвоого клиента
    '''
    client_name = StringField('Имя клиента')
    client_phone = IntegerField('Номер клиента с +7', validators=[DataRequired()])
    client_birthday = StringField('День рождения клиента')
    submit1 = SubmitField('Добавить')

    def validate_client_phone(self, client_phone):
        client = Client.query.filter_by(client_phone=client_phone.data).first()
        if client is not None:
            raise ValidationError("Такой телефон уже используется!!!")

class ClientFamilyForm(FlaskForm):
    #client_phone = IntegerField('Номер клиента', validators=[DataRequired()])
    client_family_name = StringField('Имя члена семью клиента', validators=[DataRequired()])
    client_family_birthday = StringField('День рождения члена семьи клиента', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class ClientSearchForm(FlaskForm):
    """
    Форма поиска
    """
    search = IntegerField('Поиск')
    submit2 = SubmitField('Искать')

class LoginForm(FlaskForm):
    """
    Логин форма
    """
    login = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField('Вход')


class RegistrationForm(FlaskForm):
    """
    Форма регистрации
    """
    user = StringField('USer', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Rassword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрировать')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Такая почта уже используется!!!")