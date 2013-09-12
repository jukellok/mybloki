# -*- coding: utf-8 -*-
# Copyright (c) 2013 Juha Kellokoski

import pytest

from myblog import db
import myblog.config
from models import User, Post, Tag


#def setup_module(module):

def teardown_module(module):
    db.drop_all()


class TestCase:

    def setup_method(self, method):
        db.drop_all()
        db.create_all()

    def teardown_method(self, method):
        db.session.remove()

    def test_user(self):
        user1 = User("username", "password")
        db.session.add(user1)
        db.session.commit()
        user2 = User.query.filter_by(username="username").first()
        assert user2 is not None
        assert user2.username == "username"
        assert user2.password == "password"

    def test_tag(self):
        tag1 = Tag("tagname1")
        tag2 = Tag("tagname2")
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.commit()
        tags = Tag.query.order_by(Tag.name)
        assert tags[0] is not None
        assert tags[0].name == "tagname1"
        assert tags[1] is not None
        assert tags[1].name == "tagname2"

    def test_post(self):
        post = Post("Title", "Content")
        db.session.add(post)
        db.session.commit()
        posts = Post.query.all()
        assert posts[0] is not None
        assert posts[0].title == "Title"
        assert posts[0].body == "Content"

    def test_add_tags(self):
        post = Post("Title", "Content")
        tag1 = Tag("tagname1")
        tag2 = Tag("tagname2")
        db.session.add(post)
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.commit()
        posts = Post.query.all()
        assert len(posts[0].tags) == 0
        tag3 = Tag.query.filter_by(name="tagname1").first()
        tag4 = Tag.query.filter_by(name="tagname2").first()
        assert tag1.id == tag3.id
        assert tag2.id == tag4.id
        posts[0].tags.append(tag3)
        posts[0].tags.append(tag4)
        db.session.commit()
        assert len(posts[0].tags) == 2
