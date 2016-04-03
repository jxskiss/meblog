# -*- coding: utf-8 -*-
#
# @auther: jxs <jxskiss@126.com>
# @created: 2016/4/2
#

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(Form):
    title = StringField(u'标题', validators=[DataRequired()])
    categories = StringField(u'分类')
    tags = StringField(u'标签')
    summary = TextAreaField(u'摘要')
    body = TextAreaField(u'内容', validators=[DataRequired()])
    submit = SubmitField(u'提交')
