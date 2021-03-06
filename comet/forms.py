# -*- coding: utf-8 -*-
"""
    :file: forms.py
    :time: 2021/11/17
    :author: Yingchuan Luo (罗颖川)
    :url: http://hellboycc.cn
    :copyright: © 2021 Yingchuan Luo <luoyingchuan1210@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from comet.models import Category, User


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[DataRequired(message="Username is required"),
                    Length(5, 30, message='Username length should be between 5 and 20')])
    email = StringField(
        validators=[DataRequired(message='Email is required'), Email(message='The email is wrong'),
                    Length(10, 100, message='Email length should be between 10 and 100')])
    password = PasswordField(validators=[DataRequired(message='Password is required'),
                                         Length(6, 18, message='Password length should be between 6 and 18')])
    password2 = PasswordField(
        validators=[DataRequired(message='Password is required'),
                    Length(6, 18, message='Password length should be between 6 and 18'),
                    EqualTo('password', message='Password repetition must be equal to password')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The mailbox has been registered')


class LoginForm(FlaskForm):
    email = StringField(
        validators=[DataRequired(message="Please enter email"), Email(message='The email is wrong')])
    password = PasswordField(validators=[DataRequired(message="Please enter the password"),
                                         Length(6, 18, message='Password length should be between 6 and 18')])
    remember = BooleanField()

    submit = SubmitField()


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='The category name cannot be empty'), Length(1, 50)])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 256)])
    password = PasswordField('Passowrd', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]
