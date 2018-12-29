import logging; logging.basicConfig(level=logging.INFO)

from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from ..models import User



class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')



class RegisterForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
	username = StringField('Username', validators=[DataRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only leters, numbers, dots, underscores')])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Password must match')])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already register')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Old password', validators=[DataRequired()])
	password = PasswordField('New password', validators=[DataRequired(),])
	password2 = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('password', message='Password must match')])
	submit = SubmitField('Update Password')
