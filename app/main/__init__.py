import logging; logging.basicConfig(level=logging.INFO)

from flask import Blueprint



main = Blueprint('main', __name__)



from . import views, errors