# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/4/9
#

from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from ..models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username and password
        user = User.query.filter_by(email=email_or_token).first()
        if not user:
            return False
    g.current_user = user
    return user.verify_password(password)
