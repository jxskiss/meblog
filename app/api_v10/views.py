# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/3/30
#

from flask import g, request, jsonify, url_for
from .. import db
from ..models import Post
from . import api
from .auth import auth


@api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token(expiration=3600)
    return jsonify({'token': token, 'expiration': 3600})


@api.route('/publish', methods=['POST'])
@auth.login_required
def publish():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    print(post)
    return jsonify({'status': 'ok', 'url': url_for(
        'blog.post', id=post.id, _external=True)}), 201
