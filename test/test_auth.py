# -*- coding: utf-8 -*-
"""
    :file: test_auth.py
    :time: 2021/12/04
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import url_for
from test.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('Welcome back hellboycc.', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('hellboycc logout success.', data)

    def test_fail_login_with_password_error(self):
        response = self.login(email='admin@admin.com', password='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('Login failed, please confirm whether the email or password is correct', data)

    def test_fail_login_with_account_not_exist(self):
        response = self.login(email='admin@admin.cn', password='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('No account info.', data)

    def test_login_protect(self):
        response = self.client.get(url_for('admin.manage_category'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Unauthorized', data)
