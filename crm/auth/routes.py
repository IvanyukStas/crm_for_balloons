from crm.auth import bp
from crm import db
from flask import url_for, render_template, redirect, flash
from flask_login import current_user, logout_user, login_user
from crm.models import User
from crm.auth.forms import LoginForm, RegistrationForm as rf



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.login.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Неверный юзер или пассворд')
            return redirect(url_for('auth.login'))
        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', login_form=login_form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/registration', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    reg_form = rf()
    if reg_form.validate_on_submit():
        user = User(user=reg_form.user.data, email=reg_form.email.data)
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Поздравляем с регистрацией {user.user}')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', title="Регистрация", reg_form=reg_form)
