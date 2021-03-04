from crm.main import bp
from crm import db
from flask import render_template, url_for, redirect, flash, request
from crm.main.forms import ClientForm, ClientSearchForm, ClientFamilyForm
from crm.models import Client, ClientFamily
from datetime import datetime
from flask_login import current_user, login_required

def str_to_date(date)->datetime:
    '''
    Функция приобразует строку в дату
    :param date:
    :return:
    '''
    date = datetime.strptime(date, "%d.%m.%Y")
    return date

@bp.route('/', methods=['GET','POST'])
@bp.route('/index', methods=['GET','POST'])
@login_required
def index():
    """
    Главная страница, создание нового клмента!
    """
    search = None
    form = ClientForm()
    form_search = ClientSearchForm()
    if form.validate_on_submit() and form.submit1.data:
        client = Client(client_name=form.client_name.data, client_phone=form.client_phone.data,
                        client_birthday=str_to_date(form.client_birthday.data), own_client=current_user)
        db.session.add(client)
        db.session.commit()
        flash(f'Успешно добавили нового клиента: {form.client_name.data}!!!!!!!!!')
        return redirect(url_for('main.index'))
    clients = current_user.clients
    return render_template('index.html', title='Главная', form=form, search=search, form_search=form_search, clients=clients)


@bp.route('/user/<int:client_phone>', methods=['GET', 'POST'])
@login_required
def user(client_phone):

    client_family_add_form = ClientFamilyForm()
    client_phone_in_url = request.args.get('client_phone')
    if not client_phone_in_url ==None:
        client_phone = client_phone_in_url
    client = Client.query.filter_by(client_phone=client_phone).first()
    client_family = ClientFamily.query.filter_by(client_id=client.id)
    return render_template('user.html', title=client.client_name, client=client,
                           client_family_add_form=client_family_add_form, client_family=client_family)

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form_search = ClientSearchForm()
    form = ClientForm()
    if form_search.validate_on_submit() and form_search.submit2.data:
        search = Client.query.filter_by(client_phone=form_search.search.data).first()
        return render_template('index.html', title='Главная', form=form, search=search, form_search=form_search)



@bp.route('/client_family_add', methods=['GET', 'POST'])
@login_required
def client_family_add():
    client_family_add_form = ClientFamilyForm()

    if client_family_add_form.validate_on_submit():
        client_phone = request.args.get('client_phone')
        client = Client.query.filter_by(client_phone=client_phone).first()
        client_family = ClientFamily(client_family_name=client_family_add_form.client_family_name.data,
                                     client_family_birthday=str_to_date(client_family_add_form.client_family_birthday.data),
                                     client=client)
        db.session.add(client_family)
        db.session.commit()
        flash('Успешно добавили родственника!')
        return redirect(url_for('main.user', client_phone=client_phone))
    return render_template('user.html', title='Добавить члена клиента',
                           client_family_add_form=client_family_add_form)


@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    client_phone = request.args.get('client_phone')
    family_id = request.args.get('family_id')
    family_delete = ClientFamily.query.filter_by(id=int(family_id)).first()
    print(family_delete)
    db.session.delete(family_delete)
    db.session.commit()
    return redirect(url_for('main.user', client_phone=client_phone))


@bp.route('/edit', methods=['GET', 'POST'])
def edit():
    client_phone = request.args.get('client_phone')
    family_id = request.args.get('family_id')
    edit_form = ClientFamilyForm()
    family_client = ClientFamily.query.filter_by(id=int(family_id)).first()
    client = Client.query.filter_by(client_phone=client_phone).first()
    client_family = ClientFamily.query.filter_by(client_id=client.id)
    if edit_form.validate_on_submit():
        date = datetime.strptime(edit_form.client_family_birthday.data, "%d.%m.%Y")
        family_client.client_family_name = edit_form.client_family_name.data
        family_client.client_family_birthday = date
        db.session.commit()
        return redirect(url_for('main.user', client_phone=client_phone))
    elif request.method == 'GET':
        edit_form = ClientFamilyForm(client_family_name=family_client.client_family_name,
                                     client_family_birthday = family_client.client_family_birthday.date())
    return render_template('user.html', client=client, client_family=client_family, edit_form=edit_form,
                           family_id=family_id)