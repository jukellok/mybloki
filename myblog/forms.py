# -*- coding: utf-8 -*-
# Copyright (c) 2013 Juha Kellokoski

from wtforms import Form, TextField, validators
from myblog import app

class PostForm(Form):
    title = TextField('Title', [validators.Length(min=1, max=app.config['POST_TITLE_LENGTH'])])
    body = TextField('Text', [validators.Length(min=1, max=app.config['POST_BODY_LENGTH'])])


class TagForm(Form):
    tag = TextField('Tag', [validators.Length(min=1, max=app.config['TAG_NAME_LENGTH'])])


class SearchForm(Form):
    searchfield = TextField('Search', [validators.Length(min=1)])
