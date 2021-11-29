# -*- coding: utf-8 -*-
"""
    :file: fake_data.py
    :time: 2021/11/19
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import random
from faker import Faker
from sqlalchemy.exc import IntegrityError

from comet.ext import db
from comet.models import User, Post, Category

fake = Faker()


def fake_user(count=10):
    for index in range(count):
        user = User()
        user.username = fake.name()
        user.email = fake.email()
        user.blog_title = fake.word().title()
        user.blog_sub_title = fake.sentence()
        user.about = fake.paragraph()
        user.set_password('12345678')

        db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_categories(count=10):
    for index in range(count):
        category = Category()
        category.name = fake.word()

        db.session.add(category)

    db.session.commit()


def fake_posts(count=50):
    for index in range(count):
        post = Post()
        post.title = fake.sentence()
        post.body = fake.text(2000)
        post.timestamp = fake.date_this_year()
        post.category = Category.query.get(random.randint(1, Category.query.count()))
        db.session.add(post)
    db.session.commit()
