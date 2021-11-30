# -*- coding: utf-8 -*-
"""
    :file: base.py
    :time: 2021/11/28
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import unittest
from comet import create_app
from comet.ext import db
from comet.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app(config_name='testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        # initialize db and create user
        db.create_all()
        user = User()
        user.username = 'hellboycc'
        user.email = 'admin@admin.com'
        user.set_password('12345678')
        db.session.add(user)
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.pop()
