from app import mongo
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask.ext.login import login_required, login_user, logout_user

from . import users

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
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
            mongo.db.users.insert({'email':email, 'username':uname, 'password': User.gen_passwd_hash(passwd)})
            flash('注册成功', 'SUCCESS')
            return redirect(url_for('main.index'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            db_user = mongo.db.users.find_one({'email': form.email.data})
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
@login_required
def profile():
    return render_template('profile.html')

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))