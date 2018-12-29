import logging; logging.basicConfig(level=logging.INFO)

from flask import Blueprint



auth = Blueprint('auth', __name__)



from . import views