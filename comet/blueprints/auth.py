# -*- coding: utf-8 -*-
"""
    :file: auth.py
    :time: 2021/11/18
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from comet.forms import RegisterForm, LoginForm
from comet.models import User
from comet.ext import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        # query user by email
        user = User.query.filter_by(email=email).first()
        if user:
            if user.validate_password(password):
                login_user(user, remember)
                flash(f'Welcome back {user.username}.', 'info')
                return redirect(url_for('blog.index'))

            flash(f'Invalid username or password.', 'warning')
        else:
            flash(f'No account info.', 'warning')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(f'{username} logout success.', 'info')
    return redirect(url_for('blog.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # save user
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('blog.index'))

    return render_template('register.html', form=form)
