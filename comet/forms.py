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

from comet.models import Category


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[DataRequired(message="The username can't be empty."),
                    Length(1, 20, message='The length should be between 1 and 20.')])
    email = StringField(validators=[DataRequired(), Email(message='Invaild email format.'), Length(1, 256)])
    password = PasswordField(validators=[DataRequired(), Length(1, 128)])
    password2 = PasswordField(validators=[DataRequired(), Length(1, 128), EqualTo('password')])


class LoginForm(FlaskForm):
    email = StringField(
        validators=[DataRequired(message="The email can't be empty."), Email(message='Invaild email format.')])
    password = PasswordField(validators=[DataRequired(message="The password can't be empty.")])
    remember = BooleanField()


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
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
