from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired

class PkForm(Form):
    pk1 = StringField(validators=[DataRequired()])
    pk2 = StringField(validators=[DataRequired()])
    submit = SubmitField('pk一下')

class LoginForm(Form):
    email = EmailField('邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    # recaptcha = RecaptchaField('验证码', validators=[DataRequired()])

class RegisterForm(Form):
    email = EmailField('邮箱', validators=[DataRequired()])
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    repeat = PasswordField('重复密码', validators=[DataRequired()])
    submit = SubmitField('注册')

class BaseEntryForm(Form):
    title = StringField('名称', validators=[DataRequired()])
    type = StringField('类型', validators=[DataRequired()])