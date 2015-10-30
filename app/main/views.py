from app import mongo
from app.forms import LoginForm, BaseEntryForm
from collections import defaultdict
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from flask import render_template, request, flash, url_for, abort, redirect, jsonify
from flask.ext.login import current_user, login_required
from random import randint
from util import TypeRender

from . import main
import pymongo
import re

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
            pk1_title = pk_arr[0].strip()
            pk2_title = pk_arr[1].strip()
            pk1_regx = re.compile(r'\b%s\b'%pk1_title, re.IGNORECASE)
            pk2_regx = re.compile(r'\b%s\b'%pk2_title, re.IGNORECASE)
            pk1_item = mongo.db['items'].find_one({'title': pk1_regx })
            pk2_item = mongo.db['items'].find_one({'title': pk2_regx })
            if pk1_item and pk2_item:
                # 按首字母大小排序
                rows_by_name = defaultdict(list)
                for attr in pk1_item['attributes']:
                    rows_by_name[attr['attr_name']].append(attr)
                for attr in pk2_item['attributes']:
                    # 保证顺序
                    if not attr['attr_name'] in rows_by_name.keys():
                        rows_by_name[attr['attr_name']].append({})
                    rows_by_name[attr['attr_name']].append(attr)

                for key, attrs in rows_by_name.items():
                    if len(attrs) == 1:
                        attrs.append({})

                return render_template('pk.html', pk1=pk1_item, pk2=pk2_item,\
                                       attrs=rows_by_name, TypeRender=TypeRender)
            else:
                if not pk1_item:
                    flash('搜索不到%s'%pk1_title, 'index')
                if not pk2_item:
                    flash('搜索不到%s'%pk2_title, 'index')
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
    if item:
        return redirect(url_for('.item', title=item['title']))
    return redirect(url_for('.index'))

@main.route('/search')
def search():
    q = request.args.get('q', None)
    if q is None:
        abort(404)
    keyword = q.strip()
    regx = re.compile(r'%s' %keyword, re.IGNORECASE)
    list = mongo.db['items'].find({'title': regx }).limit(20).sort('created_at', pymongo.DESCENDING)
    if list.count() == 0:
        flash('没有找到结果', 'search')
    return render_template('explore.html', items=list, title='搜索')

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

