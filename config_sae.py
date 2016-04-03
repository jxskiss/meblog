# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/4/2
#

# your private SAE settings
# put things you don't want others seeing here
#
dburl = 'mysql://{u}:{pw}@{host}:{port}/{db}?charset=utf8'

import sae
try:
    # SAE online production environment
    import sae.const
    SQLALCHEMY_DATABASE_URI = dburl.format(
        u=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS,
        host=sae.const.MYSQL_HOST, port=sae.const.MYSQL_PORT,
        db=sae.const.MYSQL_DB)
except ImportError:
    # local development environment
    SQLALCHEMY_DATABASE_URI = dburl.format(
        u='meblog', pw='meblog',
        host='localhost', port='3306', db='app_meblog')

SECRET_KEY = 'change this to your secret key'
SQLALCHEMY_POOL_RECYCLE = 10

MEBLOG_REG_CODE = 'my secret reg code'
MEBLOG_UYAN_UID = 'my personal uyan uid'
