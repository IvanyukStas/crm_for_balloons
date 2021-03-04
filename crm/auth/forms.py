from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from crm.models import User



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