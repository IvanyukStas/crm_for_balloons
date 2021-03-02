from crm import app,db
from flask import render_template, url_for, redirect, flash, request
from crm.forms import ClientForm, ClientSearchForm, LoginForm, RegistrationForm as rf, ClientFamilyForm
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
                        client_birthday=date, own_client=current_user)
        db.session.add(client)
        db.session.commit()
        flash(f'Успешно добавили нового клиента: {form.client_name.data}!!!!!!!!!')
        return redirect(url_for('index'))
    print(current_user.id)
    clients = current_user.clients
    return render_template('index.html', title='Главная', form=form, search=search, form_search=form_search, clients=clients)


@app.route('/user/<int:client_phone>', methods=['GET', 'POST'])
@login_required
def user(client_phone):

    client_family_add_form = ClientFamilyForm()
    client = Client.query.filter_by(client_phone=client_phone).first()
    print(client)
    phone = request.args.get('client_phone')
    print(phone, 'dsfdsf')
    '''client_family = ClientFamily.query.filter_by(current_user.clients.client_family)
    for client_famil in client_family:
        print(client_famil.id, client_famil.id)'''
    return render_template('user.html', title=client.client_name, client=client,
                           client_family_add_form=client_family_add_form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('index'))
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


@app.route('/client_family_add', methods=['GET', 'POST'])
@login_required
def client_family_add():
    client_family_add_form = ClientFamilyForm()
    if client_family_add_form.validate_on_submit():
        print('fsdfdsfdsfsf')
        client = Client.query.filter_by(client_phone=client_family_add_form.client_phone.data).first()
        client_family = ClientFamily(client_family_name=client_family_add_form.client_family_name.data,
                                     client_family_birthday=client_family_add_form.client_family_birthday.data,
                                     client=client)
        db.session.add(client_family)
        db.session.commit()
        print(client_family)
        flash('Успешно добавили родственника!')
        return redirect(url_for('user', client_phone=client_family_add_form.client_phone.data))
    return render_template('user.html', title='Добавить члена клиента',
                           client_family_add_form=client_family_add_form)