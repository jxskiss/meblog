# -*- coding: utf-8 -*-
#
# Copyright (c) 2016. All rights reserved.
#
# @author: jxs <jxskiss@126.com>
# @created: 16-3-30
#

from flask import render_template, redirect, url_for
from . import main


@main.route('/')
def index():
    # TODO: add index page
    return redirect(url_for('blog.index'))


@main.route('/about')
def about():
    return render_template('about.html')
