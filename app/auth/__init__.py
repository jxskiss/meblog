# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/3/31
#

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
