import logging; logging.basicConfig(level=logging.INFO)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField



class EditProfileForm(FlaskForm):
	name = StringField('Real name', validators=[Length(0,64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')



class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	body = PageDownField('Body', validators=[DataRequired()])
	submit = SubmitField('Submit')