# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/3/30
#

from flask import Blueprint

api = Blueprint('api_v10', __name__)

from . import views
