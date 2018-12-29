import logging; logging.basicConfig(level=logging.INFO)

from functools import wrap
from flask import abort
from .models import User
from flask_login import current_user



def admin_required():
	def decorator(f):
		@wrap(f)
		def decorated_function(*args, **kw):
			if not current_user.admin:
				abort(403)
			return f(*args, **kw)
		return decorated_function
	return decorator