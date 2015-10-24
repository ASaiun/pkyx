from flask import render_template, request, flash, url_for, Response
from app import mongo
from app.forms import PkForm

from . import main


@main.route('/')
def index():
    # mongo.db.items.insert({'title':'iPhone 6S', 'attributes':[{'price':'799$'}]})
    pk_form = PkForm()
    return render_template('index.html', form=pk_form)


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
    return render_template('create.html')
