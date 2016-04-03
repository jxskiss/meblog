# -*- coding: utf-8 -*-
#
# Copyright (c) 2016. All rights reserved.
#
# @author: jxs <jxskiss@126.com>
# @created: 2016-4-2
#

import sys
from os.path import join, abspath, dirname

_root = abspath(dirname(__file__))
sys.path.insert(0, join(_root, 'vendor'))


import sae
from app import create_app

# Change debug value to toggle online debug setting
myapp = create_app('sae', debug=True)

# Create new model tables, but will not touch those simply changed names,
# relationship or constraints, in case of that use manual migration in stead.
# This is useful especially for first time deployment.
from app import db
db.create_all(app=myapp)

application = sae.create_wsgi_app(myapp)
