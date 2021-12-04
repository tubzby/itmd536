# -*- coding: utf-8 -*-
"""
    :file: test_admin.py
    :time: 2021/12/04
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import url_for
from test.base import BaseTestCase
from comet.models import Category, Post
from comet.ext import db


class AdminTestCase(BaseTestCase):

    def setUp(self) -> None:
        super(AdminTestCase, self).setUp()
        self.login()

        category = Category(name='test')
        post = Post(title='Hello itmd536', body='test itmd536', category=category)

        db.session.add_all([category, post])
        db.session.commit()

    def test_new_post(self):
        response = self.client.get(url_for('admin.new_post'))
        data = response.get_data(as_text=True)
        self.assertIn('New Post', data)

        response = self.client.post(url_for('admin.new_post'), data=dict(
            title='Something',
            category=1,
            body='Hello, world.'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post created.', data)
        self.assertIn('Something', data)
        self.assertIn('Hello, world.', data)

    def test_edit_post(self):
        response = self.client.get(url_for('admin.edit_post', post_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Hello itmd536', data)
        self.assertIn('test itmd536', data)
        self.assertIn('test', data)

        response = self.client.post(url_for('admin.edit_post', post_id=1), data=dict(
            title='Something Edited',
            category=1,
            body='New post body.'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post updated.', data)
        self.assertIn('New post body.', data)
        self.assertNotIn('Blah...', data)

    def test_delete_post(self):
        response = self.client.get(url_for('admin.delete_post', post_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Post deleted.', data)
        self.assertIn('405 Method Not Allowed', data)

        response = self.client.post(url_for('admin.delete_post', post_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post deleted.', data)

    def test_new_category(self):
        response = self.client.get(url_for('admin.new_category'))
        data = response.get_data(as_text=True)
        self.assertIn('New Category', data)

        response = self.client.post(url_for('admin.new_category'), data=dict(name='Tech'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Category created.', data)
        self.assertIn('Tech', data)

        response = self.client.post(url_for('admin.new_category'), data=dict(name='Tech'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Name already in use.', data)

        category = Category.query.get(1)
        post = Post(title='Post Title', category=category)
        db.session.add(post)
        db.session.commit()
        response = self.client.get(url_for('blog.show_category', category_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Post Title', data)

    def test_edit_category(self):
        response = self.client.post(url_for('admin.new_category'), data=dict(name='Tech'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Category created.', data)
        self.assertIn('Tech', data)

        response = self.client.get(url_for('admin.edit_category', category_id=2))
        data = response.get_data(as_text=True)
        self.assertIn('Edit Category', data)
        self.assertIn('Tech', data)

        response = self.client.post(url_for('admin.edit_category', category_id=2),
                                    data=dict(name='Life'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Category updated.', data)
        self.assertIn('Life', data)
        self.assertNotIn('Tech', data)

    def test_delete_category(self):
        category = Category(name='Tech')
        post = Post(title='test', category=category)
        db.session.add(category)
        db.session.add(post)
        db.session.commit()

        response = self.client.get(url_for('admin.delete_category', category_id=1), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Category deleted.', data)
        self.assertIn('405 Method Not Allowed', data)

        response = self.client.post(url_for('admin.delete_category', category_id=2), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Category deleted.', data)
        self.assertNotIn('Tech', data)
