import logging; logging.basicConfig(level=logging.INFO)

from datetime import datetime
from flask import render_template, session, request, redirect, url_for, make_response, flash, current_app
from . import main
from .. import db
from .forms import EditProfileForm, PostForm
from ..models import User, Post, Follow_Post
from flask_login import login_required, current_user



@main.route('/', methods=['GET', 'POST'])
def index():
	posts = []
	pagination = None;
	if current_user.is_authenticated:
		page = request.args.get('page', 1, type=int)
		pagination = current_user.following_posts.order_by(Follow_Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
		posts = [item.followed for item in pagination.items]
	return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username = username).first_or_404()
	posts = user.posts.order_by(Post.timestamp.desc()).all()
	return render_template('user.html', user = user, posts = posts)



@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user._get_current_object())
		db.session.commit()
		flash('Your profile has been updated')
		return redirect(url_for('main.user', username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me = current_user.about_me
	return render_template('edit_profile.html', form=form)



@main.route('/create-blog', methods=['GET', 'POST'])
@login_required
def create_blog():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data, author=current_user._get_current_object())
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('main.index'))
	return render_template('edit_blog.html', form=form)



@main.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
	form = PostForm()
	post = Post.query.get_or_404(id)
	if form.validate_on_submit():
		post.body = form.body.data
		post.title = form.title.data
		db.session.add(post)
		db.session.commit()
		flash('The post has been updated')
		return redirect(url_for('main.index'))
	form.body.data = post.body
	form.title.data = post.title
	return render_template('edit_blog.html', form=form)



@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', post=post)


@main.route('/all_posts', methods = ['GET', 'POST'])
def all_posts():
	page = request.args.get('page', 1, type = int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page = current_app.config['FLASKY_POSTS_PER_PAGE'], error_out = False)
	posts = pagination.items
	return render_template('all_posts.html', posts = posts, pagination = pagination)


@main.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('main.index'))
	if current_user.is_following(user):
		flash('You are already following this user.')
		return redirect(url_for('main.user', username=username))
	current_user.follow(user)
	flash('You are now following %s.' % username)
	return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('main.index'))
	if not current_user.is_following(user):
		flash('You have not followed this user.')
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(user)
	flash('You are now unfollowing %s' % username)
	return redirect(url_for('main.user', username=username))


@main.route('/follow_post/<int:id>')
@login_required
def follow_post(id):
	post = Post.query.get_or_404(id)
	if post is None:
		flash('Invalid post.')
		return redirect(url_for('main.index'))
	if current_user.is_following_post(post):
		flash('You are already following this post.')
		return redirect(url_for('main.post', id=post.id))
	current_user.follow_post(post)
	flash('You are now following this blog.')
	return redirect(url_for('main.post', id=post.id))


@main.route('/unfollow_post/<int:id>')
@login_required
def unfollow_post(id):
	post = Post.query.get_or_404(id)
	if post is None:
		flash('Invalid post.')
		return redirect(url_for('main.index'))
	if not current_user.is_following_post(post):
		flash('You have not followed this blog.')
		return redirect(url_for('main.post', id=post.id))
	current_user.unfollow_post(post)
	flash('You are now unfollowing this blog.')
	return redirect(url_for('main.post', id=post.id))