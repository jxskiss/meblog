# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/3/30
#

from datetime import datetime
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from collections import namedtuple
from . import db, login_manager


Role = namedtuple('Role', ('admin', 'user'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __roles__ = Role('admin', 'user')
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role = db.Column(db.String(12))
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)
    member_since = db.Column(db.DateTime, default=datetime.now)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.role = self.__roles__.user

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def is_administrator(self):
        return self.role == 'admin'


class AnonymousUser(AnonymousUserMixin):

    @staticmethod
    def is_administrator():
        return False


tagged = db.Table(
    'tagged',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey(
        'tags.id', onupdate='CASCADE', ondelete='CASCADE'))
)


categorized = db.Table(
    'categorized',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('category_id', db.Integer, db.ForeignKey(
        'categories.id', onupdate='CASCADE', ondelete='CASCADE'))
)


def md2html(md):
    return markdown(md, output_format='html', extensions=[
        'markdown.extensions.extra'])


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_time = db.Column(db.DateTime, default=datetime.now)
    last_update = db.Column(db.DateTime, default=datetime.now)
    summary = db.Column(db.String(1024))
    summary_html_cache = db.Column(db.String(1024))
    body = db.Column(db.Text)
    body_html_cache = db.Column(db.Text)
    tags = db.relationship(
        'Tag',
        secondary=tagged,
        backref=db.backref('tags', lazy='dynamic'),
        lazy='select'
    )
    categories = db.relationship(
        'Category',
        secondary=categorized,
        backref=db.backref('categories', lazy='dynamic'),
        lazy='select'
    )

    def __init__(self, **kwargs):
        fields = kwargs.copy()
        if 'tags' in fields:
            fields['tags'] = Tag.get_tags(fields['tags'])
        if 'categories' in fields:
            fields['categories'] = Category.get_cats(fields['categories'])
        super(Post, self).__init__(**fields)

    @property
    def body_html(self):
        if not self.body:
            return None
        if not self.body_html_cache:
            self.body_html_cache = md2html(self.body)
            db.session.add(self)
            db.session.commit()
        return self.body_html_cache

    @property
    def summary_html(self):
        if not self.summary:
            return None
        if not self.summary_html_cache:
            self.summary_html_cache = md2html(self.summary)
            db.session.add(self)
            db.session.commit()
        return self.body_html_cache

    def touch(self):
        self.body_html_cache = None
        self.summary_html_cache = None
        db.session.add(self)
        db.session.commit()

    def date(self, type='u'):
        dt = {'u': self.last_update, 'p': self.post_time}
        return dt[type].strftime('%Y-%m-%d')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html_cache = md2html(value) if value else None

    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiator):
        target.summary_html_cache = md2html(value) if value else None


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Tag %s>' % self.name

    @classmethod
    def get_tags(cls, seq):
        if not seq:
            return []
        if isinstance(seq, list) and isinstance(seq[0], cls):
            return seq
        tags = []
        new_tags = []
        _seq = [t.strip() for t in seq.split(',')] if isinstance(seq, str) or \
            isinstance(seq, unicode) else (seq if isinstance(seq, list) else [])
        for t in filter(lambda x: x, _seq):
            tag = cls.query.filter_by(name=t).first()
            if not tag:
                tag = cls(name=t)
                new_tags.append(tag)
            tags.append(tag)
        db.session.add_all(new_tags)
        db.session.flush()
        return tags


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Category %s>' % self.name

    @classmethod
    def get_cats(cls, seq):
        if not seq:
            return []
        if isinstance(seq, list) and isinstance(seq[0], cls):
            return seq
        cats = []
        new_cats = []
        _seq = [c.strip() for c in seq.split(',')] if isinstance(seq, str) or \
            isinstance(seq, unicode) else (seq if isinstance(seq, list) else [])
        for c in filter(lambda x: x, _seq):
            cat = cls.query.filter_by(name=c).first()
            if not cat:
                cat = cls(name=c)
                new_cats.append(cat)
            cats.append(cat)
        db.session.add_all(new_cats)
        db.session.flush()
        return cats


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.summary, 'set', Post.on_changed_summary)
