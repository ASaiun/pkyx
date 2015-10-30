from app import mongo
from app.forms import LoginForm, BaseEntryForm
from datetime import datetime
from flask import render_template, request, flash, url_for, abort, redirect, jsonify
from flask.ext.login import current_user, login_required
from random import randint
from util import TypeRender

from . import main
import pymongo

@main.route('/')
def index():
    lg_form = LoginForm()
    return render_template('index.html', lg_form=lg_form, title='首页')


@main.route('/pk', methods=['GET', 'POST'])
def pk():
    if request.method == 'POST':
        pk_str = request.form.get('pk').strip().replace('PK', 'pk')
        pk_arr = pk_str.split('pk')
        if len(pk_arr) == 2:
            pk1_title, pk2_title = pk_arr
            pk1_data = mongo.db['items'].find({'title': pk1_title.strip()})
            pk2_data = mongo.db['items'].find({'title': pk2_title.strip()})
            return render_template('pk.html', pk1=pk1_title, pk2=pk2_title)
        else:
            flash('非法输入', 'index')
    return redirect(url_for('.index'))

@main.route('/explore')
def explore():
    items = mongo.db['items'].find().limit(20).sort('created_at', pymongo.DESCENDING)
    return render_template('explore.html', items=items, title='发现')

@main.route('/lucky')
def lucky():
    # 总条数
    N = mongo.db['items'].count()
    item = mongo.db['items'].find().limit(1).skip(randint(0, N-1))[0]
    print(item)
    if item:
        return redirect(url_for('.item', title=item['title']))
    return redirect(url_for('.index'))

@main.route('/search')
def search():
    q = request.args.get('q', None)
    if q is None:
        abort(404)
    list = mongo.db['items'].find({'title': {"$regex": q } }).limit(20).sort('created_at', pymongo.DESCENDING)
    if list.count() == 0:
        flash('没有找到结果', 'search')
    return render_template('explore.html', items=list)

@main.route('/item/<title>')
def item(title):
    item = mongo.db['items'].find_one({'title': title})
    if not item:
        abort(404)
    mongo.db['items'].update({'title': title}, {"$inc": {"view": 1}})
    return render_template('item.html', item=item, TypeRender=TypeRender)

@main.route('/item/edit_attr', methods=['POST'])
def edit_attr():
    if request.method == 'POST':
        title = request.json['title']
        attr_name = request.json['attr_name']
        attr_type = request.json['attr_type']
        attr_value = request.json['attr_value']
        if attr_value is None:
            return jsonify(status=False, reason="属性值不能为空")
        result = mongo.db['items'].update(
                {'title': title, "attributes.attr_name": attr_name},
                {
                    '$set':
                        {
                            'attributes.$':
                                {
                                    'attr_name': attr_name,
                                    'attr_value': attr_value,
                                    'attr_type': attr_type
                                }
                        }
                }
            )
        if result:
            return jsonify(status=True, reason="修改属性成功")
        else:
            return jsonify(status=True, reason="修改失败")

@main.route('/item/del_attr', methods=['POST'])
def del_attr():
    if request.method == 'POST':
        title = request.json['title']
        attr_name = request.json['attr_name']
        result = mongo.db['items'].update(
                {'title': title},
                {
                    '$pull':
                    {
                        'attributes': {'attr_name': attr_name}
                    }
                }
            )
        if result:
            return jsonify(status=True, reason="删除属性成功")
        else:
            return jsonify(status=True, reason="删除失败")


@main.route('/item/add_attr', methods=['POST'])
def add_attr():
    if request.method == 'POST':
        title = request.json['title']
        attr_name = request.json['attr_name'].strip()
        attr_type = request.json['attr_type']
        attr_value = request.json['attr_value']
        if attr_value is None:
            return jsonify(status=False, reason="属性值不能为空")
        if mongo.db['items'].find_one({'title': title, 'attributes.attr_name': attr_name}):
            return jsonify(status=False, reason="属性已存在")
        mongo.db['items'].update(
            {'title': title},
            {
                '$inc': {'attr_count': 1},
                '$push':
                    {
                        'attributes':
                            {
                                'attr_name': attr_name,
                                'attr_value': attr_value,
                                'attr_type': attr_type
                            }
                    }
            }
        )
        html = TypeRender.render_html(attr_name, attr_value, attr_type)
        return jsonify(status=True, reason="添加属性成功", html=html)

@main.route('/create_entry', methods=['GET', 'POST'])
@login_required
def create_entry():
    entry_form = BaseEntryForm()
    if entry_form.validate_on_submit():
        title = request.form['title']
        type = request.form['type']
        mongo.db.items.insert({
            'title': title,
            'type': type,
            'attributes':[],
            'attr_count': 1,
            'view': 0,
            'created_at': datetime.utcnow(),
            'created_by': current_user.id
        })
        return redirect(url_for('.item', title=title))
    return render_template('create.html', entry_form=entry_form, title='创建条目')

