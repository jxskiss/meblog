# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/3/31
#

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import current_user as cu
from . import auth
from .forms import LoginForm, RegForm
from .. import db
from ..models import User


@auth.before_app_request
def before_request():
    if cu.is_authenticated:
        cu.ping()


@auth.route('/')
def index():
    if cu.is_authenticated:
        return redirect(url_for('main.index'))
    return redirect(url_for('.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(url_for('main.index'))
        flash(u'用户名或密码验证失败，请重新登录')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'注册成功')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/reg.html', form=form)
