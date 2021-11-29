# -*- coding: utf-8 -*-
"""
    :file: ext.py
    :time: 2021/11/18
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
bootstrap = Bootstrap()
ckeditor = CKEditor()


@login_manager.user_loader
def load_user(user_id):
    from comet.models import User
    user = User.query.get(int(user_id))
    return user
