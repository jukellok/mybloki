# -*- coding: utf-8 -*-
# Copyright (c) 2013 Juha Kellokoski

import os
from myblog import app

app.config.update(
    DEBUG=False,  # Never to be used on production machines!
    SECRET_KEY='The secret key',
    #SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://username:password@localhost/mydatabase',
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL','postgres://username:password@localhost/mydatabase'),
    POST_TITLE_LENGTH=100,
    POST_BODY_LENGTH=1000,
    TAG_NAME_LENGTH=50
)
