# -*- coding: utf-8 -*-
"""
    :file: cli_testing.py
    :time: 2021/11/29
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from test.base import BaseTestCase
from comet.ext import db


class CLITestCase(BaseTestCase):

    def setUp(self) -> None:
        super(CLITestCase, self).setUp()

        db.drop_all()

    def test_init_db_command(self):
        result = self.runner.invoke(args=['init-db'])
        self.assertIn(f'Initializing the database.', result.output)

    def test_init_db_command_with_drop(self):
        result = self.runner.invoke(args=['init-db', '--drop'], input='y\n')
        self.assertIn(f'This action will delete the database, do you want to continue?', result.output)
        self.assertIn(f'delete tables.', result.output)

    def test_init_user_command(self):
        db.create_all()

        result = self.runner.invoke(
            args=['init-user', '--username', 'hellboycc', '--email', 'admin@admin.com', '--password', '12345678'])

        self.assertIn(f'Creating the temporary user account...', result.output)
        self.assertIn(f'Done', result.output)
