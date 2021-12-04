# -*- coding: utf-8 -*-
"""
    :file: test_blog.py
    :time: 2021/12/04
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from test.base import BaseTestCase
from flask import url_for
from comet.models import Category, Post
from comet.ext import db


class BlogTestCase(BaseTestCase):

    def setUp(self) -> None:
        super(BlogTestCase, self).setUp()

        self.login()

        category = Category(name='test')
        post = Post(title='Hello itmd536', body='test itmd536', category=category)

        db.session.add_all([category, post])
        db.session.commit()

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Home', data)
        self.assertIn('About', data)
        self.assertIn('test', data)
        self.assertIn('Hello itmd536', data)
        self.assertIn('test itmd536', data)

    def test_post_page(self):
        response = self.client.get(url_for('blog.show_post', post_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Hello itmd536', data)
        self.assertIn('test itmd536', data)
        self.assertIn('test', data)

    def test_about_page(self):
        response = self.client.get(url_for('blog.about'))
        data = response.get_data(as_text=True)
        self.assertIn('ITMD536 - Group One', data)
        self.assertIn('Github', data)
        self.assertIn('https://github.com/tubzby/itmd536', data)

    def test_category_page(self):
        response = self.client.get(url_for('blog.show_category', category_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Category: test', data)
        self.assertIn('Hello itmd536', data)
