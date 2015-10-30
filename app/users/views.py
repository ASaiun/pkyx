from app import mongo
from app.forms import LoginForm, RegisterForm, ProfileForm
from app.models import User
from datetime import datetime
from gridfs import GridFS, NoFile
from flask import render_template, redirect, url_for, request, flash, jsonify, abort, make_response
from flask.ext.login import login_required, login_user, logout_user, current_user
from util import bson_obj_id, AllowFile
from werkzeug.utils import secure_filename
from . import users

@users.route('/sign_up', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    lg_form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            uname = form.username.data
            passwd = form.password.data
            rp_passwd = form.repeat.data
            if passwd != rp_passwd:
                flash('两次密码不相同', 'WARNING')
            elif mongo.db.users.find_one({'email':email}) is not None:
                flash('该邮箱已被注册', 'WARNING')
            else:
                id = mongo.db['users'].insert({
                    'email':email,
                    'username':uname,
                    'password': User.gen_passwd_hash(passwd),
                    'avatar': '',
                    'join': datetime.utcnow()
                })
                if id is not None:
                    user = User(bson_obj_id(id))
                    login_user(user)
                    return redirect(url_for('main.index'))
                flash('注册失败', 'WARNING')
        else:
            for field, error in form.errors.items():
                flash("%s: %s" %(getattr(form, field).label.text, error), 'WARNING')
    return render_template('register.html', form=form, lg_form=lg_form)

@users.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            db_user = mongo.db['users'].find_one({'email': form.email.data})
            if db_user is not None:
                db_passwd = db_user.get('password', None)
                if User.verify_passwd(db_passwd, form.password.data):
                    user = User(db_user['_id'])
                    login_user(user)
                    return jsonify(status=True, reason="登录成功", redirect_url=url_for('main.index'))
                else:
                    return jsonify(status=False, reason="邮箱或密码错误")
            else:
                return jsonify(status=False, reason="不存在该用户")
        return jsonify(status=False, reason="登录失败")

@users.route('/profile')
@users.route('/profile/<id>')
def profile(id=None):
    user = None
    if id is None:
        if current_user is not None:
            return redirect(url_for('.profile', id=current_user.id))
    else:
        user = mongo.db['users'].find_one({'_id': bson_obj_id(id)})
    return render_template('profile.html', user=user)

@users.route('/profile/edit', methods=['GET','POST'])
@login_required
def profile_edit():
    user = mongo.db['users'].find_one({'_id': bson_obj_id(current_user.id)})
    if not user:
        abort(404)
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            location = form.location.data
            website = form.website.data
            introduction = form.introduction.data
            data = {
                'username': username,
                'location': location,
                'website': website,
                'introduction': introduction
            }

            avatar = request.files['avatar']
            avatar_id = None
            if avatar and AllowFile.is_img(avatar.filename):
                filename = secure_filename(avatar.filename)
                fs = GridFS(mongo.db, collection="avatar")
                fs.find()
                avatar_id = fs.put(avatar, content_type=avatar.content_type, filename=filename)
                if avatar_id:
                    if user['avatar']:
                        fs.delete(bson_obj_id(user['avatar']))
                    data['avatar'] = avatar_id
            else:
                flash('图片格式不支持')


            mongo.db['users'].update(
                {'_id': user['_id'] },
                {
                    "$set": data
                }
            )
            return redirect(url_for('.profile'))
        else:
            flash('资料修改失败', 'edit')
    return render_template('profile_edit.html', user=user, form=form, title='编辑资料')

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/static/avatar/<oid>')
def avatar(oid):
    if oid is None:
        print('oh')
        return ''
    try:
        fs = GridFS(mongo.db, "avatar")
        img = fs.get(bson_obj_id(oid))
        response = make_response(img.read())
        response.headers['Content-Type'] = img.content_type
        return response
    except NoFile:
        abort(404)
