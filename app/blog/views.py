# -*- coding: utf-8 -*-
#
# Copyright (c) 2016. All rights reserved.
#
# @author: jxs <jxskiss@126.com>
# @created: 16-3-30
#

from datetime import datetime
from flask import render_template, redirect, url_for, request, current_app
from flask.ext.login import login_required, current_user
from werkzeug.contrib.atom import AtomFeed
from .. import db
from ..models import Post, Tag, Category, md2html
from . import blog
from .forms import PostForm


@blog.route('/')
@blog.route('/<int:page>/', methods=['GET'])
def index(page=1):
    query = Post.query.order_by(Post.post_time.desc())
    pagination = query.paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('blog/blog.html', posts=posts, pagination=pagination)


@blog.route('/post/<id>')
def post(id):
    post = Post.query.options(db.joinedload('tags')).options(
        db.joinedload('categories')).get_or_404(id)
    if not post.body_html:
        post.body_html = md2html(post.body)
        db.session.add(post)
        db.session.commit()
    return render_template('blog/post.html', post=post)


@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            author_id=current_user.id,
            summary=form.summary.data,
            body=form.body.data,
            tags=Tag.get_tags(form.tags.data),
            categories=Category.get_cats(form.categories.data)
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post', id=post.id))
    return render_template('blog/edit.html', form=form)


@blog.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.filter_by(id=id).first()
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.summary = form.summary.data
        post.body = form.body.data
        post.tags = Tag.get_tags(form.tags.data)
        post.categories = Category.get_cats(form.categories.data)
        post.last_update = datetime.now()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.summary.data = post.summary
    form.body.data = post.body
    form.tags.data = ', '.join([t.name for t in post.tags])
    form.categories.data = ', '.join([c.name for c in post.categories])
    return render_template('blog/edit.html', post=post, form=form)


@blog.route('/atom.xml')
def atom_feed():
    feed = AtomFeed(u'最新文章', feed_url=request.url, url=request.url_root)
    posts = Post.query.order_by(db.desc('post_time')).limit(10).all()
    for p in posts:
        feed.add(
            title=p.title,
            content=unicode(p.body_html), content_type='html',
            summary=unicode(p.summary_html), summary_type='html',
            author=p.author.username,
            url=url_for('blog.post', id=p.id, _external=True),
            updated=p.last_update)
    return feed.get_response()
