# -*- coding: utf-8 -*-
"""
    :file: models.py
    :time: 2021/11/17
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from comet.ext import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, comment="User's ID")
    username = db.Column(db.String(50), nullable=False, comment="User's name")
    email = db.Column(db.String(256), nullable=False, comment="User's email")
    password_hash = db.Column(db.String(256), nullable=False, comment="User's password")
    blog_title = db.Column(db.String(56))
    blog_sub_title = db.Column(db.String(100))
    about = db.Column(db.Text)

    # relationship between user and post
    # posts = db.relationship('Post', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    posts = db.relationship('Post', back_populates='category', cascade='all, delete-orphan')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
