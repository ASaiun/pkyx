from flask import render_template, request, flash, url_for, current_app
from app import mongo
from app.forms import PkForm, LoginForm

from . import main


@main.route('/')
def index():
    pk_form = PkForm()
    lg_form = LoginForm()
    return render_template('index.html', pk_form=pk_form, lg_form=lg_form)


@main.route('/pk', methods=['GET', 'POST'])
def pk():
    pk_form = PkForm(request.form)
    if pk_form.validate_on_submit():
        pk1_name = request.form.get('pk1').strip()
        pk2_name = request.form.get('pk2').strip()
        pk1_data = mongo.db.items.find({'title': pk1_name})
        pk2_data = mongo.db.items.find({'title': pk2_name})
        print(url_for('api.item_api'))
        flash('查询成功', 'SUCCESS')
        return render_template('pk.html', pk1=pk1_name, pk2=pk2_name)
    flash('非法请求', 'WARNING')
    return render_template('pk.html')


@main.route('/create_entry', methods=['GET', 'POST'])
def create_entry():
    if request.method == 'POST':
        title = request.form.pop('title')
        type = request.form.pop('type')
        # mongo.db.items.insert({'title':XXX, 'attributes':[{'XX':'XXXX'}]})
    types = current_app.config['ATTR_TYPES'].values()
    return render_template('create.html', types=types)
