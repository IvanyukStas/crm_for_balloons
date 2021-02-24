from crm import app,db
from flask import render_template, url_for, redirect, flash
from crm.forms import CientForm
from crm.models import Client, ClientFamily


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    """
    Главная страница, создание нового клмента!
    """
    form = CientForm()
    if form.validate_on_submit():
        client = Client(client_name=form.client_name.data, client_phone=form.client_phone.data,
                        client_birthday=form.client_birthday.data)
        db.session.add(client)
        db.session.commit()
        flash(f'Успешно добавили нового клиента: {form.client_name.data}!!!!!!!!!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Главная', form=form)