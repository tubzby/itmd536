# -*- coding: utf-8 -*-
"""
    :file: settings.py
    :time: 2021/11/18
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import sys

# base dir
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# print(BASE_DIR)

# SQLite URI adapter
WIN_OS = sys.platform.startswith('win')

if WIN_OS:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# Base config
class BaseConfig(object):
    # secret key for web app
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    # config for SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # pagination config for Quokka
    BLOG_POST_PER_PAGE = 6
    BLOG_MANAGE_POST_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(BASE_DIR, 'comet-dev.db')
    WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
