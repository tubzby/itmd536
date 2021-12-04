# -*- coding: utf-8 -*-
"""
    :file: test_settings.py
    :time: 2021/12/04
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import sys
from flask import current_app
from comet import create_app

from test.base import BaseTestCase


class BasicTestCase(BaseTestCase):

    def test_app_exist(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_config_name_with_none(self):
        app = create_app()
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        self.assertTrue(current_app.config['DEV'])

    def test_app_os_platform(self):
        self.assertFalse(sys.platform.startswith('win'))
