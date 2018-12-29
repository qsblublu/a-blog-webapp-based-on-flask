from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:qushuo@localhost/webapp'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)



class Follow(db.Model):
	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Follow_Post(db.Model):
	__tablename__ = 'follow_posts'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	admin = db.Column(db.Integer, default=0)

	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text)
	member_since = db.Column(db.DateTime, default=datetime.utcnow)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)

	following = db.relationship('Follow', 
								foreign_keys=[Follow.follower_id],
								backref=db.backref('follower', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	followers = db.relationship('Follow',
								foreign_keys=[Follow.followed_id],
								backref=db.backref('followed', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	posts = db.relationship('Post', backref='author', lazy='dynamic')

	following_posts = db.relationship('Follow_Post',
								   foreign_keys=[Follow_Post.follower_id],
								   backref=db.backref('follower', lazy='joined'),
								   lazy='dynamic',
								   cascade='all, delete-orphan')

	def __repr__(self):
		return '<User %r>' % self.username

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def is_administator(self):
		return self.admin

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)
		db.session.commit()

	def follow(self, user):
		if not is_following(user):
			f = Follow(follower=self, followed=user)
			db.session.add(f)

	def unfollow(self, user):
		f = self.following.filter_by(followed_id=user.id).first()
		if f:
			db.session.delete(f)

	def is_following(self, user):
		return self.following.filter_by(followed_id=user.id).first() is not None

	def is_followed_by(self, user):
		return self.followers.filter_by(follower_id=user.id).first() is not None

	def follow_post(self, post):
		if not is_following_post(post):
			f = Follow_Post(follower=self, followed=post)
			db.session.add(f)
		
	def unfollow_post(self, post):
		f = self.following_posts.filter_by(followed_id=post.id)
		if f:
			db.session.delete(f)

	def is_following_post(self, post):
		return self.following_posts.filter_by(followed_id=post.id) is not None


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	body_html = db.Column(db.Text)

	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	followers = db.relationship('Follow_Post',
								foreign_keys=[Follow_Post.followed_id],
								backref=db.backref('followed', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	@staticmethod
	def on_changed_body(target, value, oldvalue, initator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))



db.event.listen(Post.body, 'set', Post.on_changed_body)



if __name__ == '__main__':
    db.drop_all()
    db.create_all()