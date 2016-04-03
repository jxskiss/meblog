# -*- coding: utf-8 -*-
#
# Copyright (c) 2016. All rights reserved.
#
# @author: jxs <jxskiss@126.com>
# @created: 16-3-30
#

from os.path import join, abspath, dirname
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

_root = abspath(dirname(__file__))
_tmpl = join(_root, 'templates')
_static = join(dirname(_root), 'static')


# NullPool SQLAlchemy class for environments without database connections
# pool support, such as SAE.
# Without this you may get (2006, 'MySQL server has gone away') errors.
class NullPoolSQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(NullPoolSQLAlchemy, self).apply_driver_hacks(app, info, options)
        from sqlalchemy.pool import NullPool
        options['poolclass'] = NullPool
        del options['pool_size']

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name, **kwargs):
    app = Flask(__name__, template_folder=_tmpl, static_folder=_static)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.update(kwargs)

    # init flask extensions
    global db
    if app.config.get('MEBLOG_USE_NULLPOOL', None):
        db = NullPoolSQLAlchemy()
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .blog import blog as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    from .api_v10 import api as api_v10
    app.register_blueprint(api_v10, url_prefix='/api/v1.0')

    return app
