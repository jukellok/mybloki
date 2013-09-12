# -*- coding: utf-8 -*-
# Copyright (c) 2013 Juha Kellokoski

from datetime import datetime
from flask.ext.login import UserMixin
from myblog import db, app

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(16))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError("No 'id' attribute - override 'get_id'")

    def __eq__(self, other):
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(app.config['POST_TITLE_LENGTH']))
    body = db.Column(db.String(app.config['POST_BODY_LENGTH']))
    timestamp = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(app.config['TAG_NAME_LENGTH']))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name
