# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/4/2
#

from flask import current_app
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[
        DataRequired(), EqualTo('confirm', message=u'两次输入密码不匹配')])
    confirm = PasswordField(u'确认密码', validators=[DataRequired()])
    regcode = StringField(u'注册码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已经注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被使用')

    def validate_regcode(self, field):
        if field.data != current_app.config['MEBLOG_REG_CODE']:
            raise ValidationError(u'注册码错误')
