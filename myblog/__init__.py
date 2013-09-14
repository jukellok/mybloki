# -*- coding: utf-8 -*-
# Copyright (c) 2013 Juha Kellokoski

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
import myblog.config
db = SQLAlchemy(app)
import myblog.views
