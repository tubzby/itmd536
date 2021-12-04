# -*- coding: utf-8 -*-
"""
    :file: test_cli.py
    :time: 2021/11/29
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from test.base import BaseTestCase
from comet.ext import db
from comet.models import User, Post, Category


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
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'hellboycc')
        self.assertEqual(User.query.first().email, 'admin@admin.com')
        self.assertTrue(User.query.first().validate_password('12345678'))

    def test_init_user_with_upate(self):
        db.create_all()

        self.runner.invoke(
            args=['init-user', '--username', 'hellboycc', '--email', 'admin@admin.com', '--password', '12345678'])
        result = self.runner.invoke(
            args=['init-user', '--username', 'new hellboycc', '--email', 'admin@admin.com', '--password', '12345678'])
        self.assertIn(f'The user already exists, updating...', result.output)
        self.assertNotIn('Creating the temporary user account...', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'new hellboycc')
        self.assertEqual(User.query.first().email, 'admin@admin.com')
        self.assertTrue(User.query.first().validate_password('12345678'))

    def test_forge_command(self):
        db.create_all()

        result = self.runner.invoke(args=['forge'])
        self.assertEqual(User.query.count(), 10)
        self.assertIn('Generating 10 users...', result.output)

        self.assertEqual(Category.query.count(), 10)
        self.assertIn('Generating 10 categories...', result.output)

        self.assertEqual(Post.query.count(), 50)
        self.assertIn('Generating 50 posts...', result.output)

        self.assertIn('Done.', result.output)

    def test_forge_command_with_count(self):
        db.create_all()

        result = self.runner.invoke(args=['forge', '--user', '5', '--category', '20', '--post', '100'])
        self.assertEqual(User.query.count(), 5)
        self.assertIn('Generating 5 users...', result.output)

        self.assertEqual(Category.query.count(), 20)
        self.assertIn('Generating 20 categories...', result.output)

        self.assertEqual(Post.query.count(), 100)
        self.assertIn('Generating 100 posts...', result.output)

        self.assertIn('Done.', result.output)
