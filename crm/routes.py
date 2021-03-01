from crm import app,db
from flask import render_template, url_for, redirect, flash
from crm.forms import ClientForm, ClientSearchForm, LoginForm, RegistrationForm as rf
from crm.models import Client, ClientFamily, User
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    """
    Главная страница, создание нового клмента!
    """
    search = None
    form = ClientForm()
    form_search = ClientSearchForm()
    if form.validate_on_submit() and form.submit1.data:
        date = datetime.strptime(form.client_birthday.data, "%d.%m.%Y")
        client = Client(client_name=form.client_name.data, client_phone=form.client_phone.data,
                        client_birthday=date)
        db.session.add(client)
        db.session.commit()
        flash(f'Успешно добавили нового клиента: {form.client_name.data}!!!!!!!!!')
        return redirect(url_for('index'))
    clients = Client.query.all()
    return render_template('index.html', title='Главная', form=form, search=search, form_search=form_search, clients=clients)


@app.route('/user/<client_phone>', methods=['GET', 'POST'])
def user(client_phone):
    client = Client.query.filter_by(client_phone=client_phone).first()
    print(client)
    return render_template('user.html', title=client.client_name, client=client)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form_search = ClientSearchForm()
    form = ClientForm()
    if form_search.validate_on_submit() and form_search.submit2.data:
        search = Client.query.filter_by(client_phone=form_search.search.data).first()
        return render_template('index.html', title='Главная', form=form, search=search, form_search=form_search)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.login.data).first()
        print(user.email, user.password_hash)
        print(login_form.login.data, login_form.password.data)
        if user is None or not user.check_password(login_form.password.data):
            flash('Неверный юзер или пассворд')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        redirect(redirect('index'))
    return render_template('login.html', title='Login', login_form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/registration', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = rf()
    if reg_form.validate_on_submit():
        user = User(user=reg_form.user.data, email=reg_form.email.data)
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Поздравляем с регистрацией {user.user}')
        return redirect(url_for('login'))
    return render_template('registration.html', title="Регистрация", reg_form=reg_form)