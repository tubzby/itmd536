# -*- coding: utf-8 -*-
"""
    :file: __init__.py.py
    :time: 2021/11/18
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os
from flask import Flask
import click

from comet.settings import config_dict
from comet.ext import db, migrate, login_manager, moment, bootstrap, ckeditor
from comet.models import User, Category
from comet.blueprints.blog import blog_bp
from comet.blueprints.auth import auth_bp
from comet.blueprints.admin import admin_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    _register_extensions(app)
    _register_blueprints(app)
    _register_commands(app)
    _register_template_ctx(app)

    return app


def _register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    ckeditor.init_app(app)


def _register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def _register_template_ctx(app):
    @app.context_processor
    def make_template_ctx():
        categories = Category.query.order_by(Category.name).all()

        return dict(categories=categories)


def _register_commands(app):
    @app.cli.command()
    @click.option('--username', prompt=True, help="The user's name")
    @click.option('--email', prompt=True, help='The email used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init_user(username, email, password):

        user = User.query.filter_by(email=email).first()
        if user is not None:
            click.echo('The user already exists, updating...')
            user.username = username
            user.email = email
            user.set_password(password)
        else:
            click.echo('Creating the temporary user account...')
            user = User()
            user.set_password(password)
            user.username = username
            user.email = email

            user.blog_title = 'comet'
            user.blog_sub_title = "No, I'm the real thing."
            user.about = 'Anything is impossble.'

            db.session.add(user)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of user, default is 10.')
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    def forge(user, category, post):

        from comet.fake_data import fake_user, fake_posts, fake_categories
        click.echo(f'Generating {user} users...')
        fake_user(user)

        click.echo(f'Generating {category} categories...')
        fake_categories(category)

        click.echo(f'Generating {post} posts...')
        fake_posts(post)

        click.echo('Done.')

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create db after drop.')
    def init_db(drop):

        if drop:
            click.confirm('This action will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('delete tables.')

        db.create_all()
        click.echo('Initializing the database.')
