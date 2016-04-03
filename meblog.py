# -*- coding: utf-8 -*-
#
# Copyright (c) 2016. All rights reserved.
#
# @author: jxs <jxskiss@126.com>
# @created: 16-3-30
#

# Local development manager script
# this file will not be executed on production server
#
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Post, Tag, Category

myapp = create_app(os.getenv('MEBLOG_CONFIG') or 'default')
manager = Manager(myapp)
migrate = Migrate(myapp, db)


def make_shell_context():
    return dict(
        app=myapp, db=db, User=User, Post=Post, Tag=Tag, Category=Category
    )

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
