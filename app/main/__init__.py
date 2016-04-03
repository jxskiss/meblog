# -*- coding: utf-8 -*-
#
# Copyright (c) 2016. All rights reserved.
#
# @author: jxs <jxskiss@126.com>
# @created: 16-3-30
# 

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
