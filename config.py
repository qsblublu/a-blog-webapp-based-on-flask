import os



basedir = os.path.abspath(os.path.dirname(__file__))



class Config(dict):
	#create flask-wtf secret_key
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
	FLASKY_POSTS_PER_PAGE = 10

	@staticmethod
	def init_app(app):
		pass



class DevelopmentConfig(Config):
	#set debug model of app run to the true
	DEBUG = True
	#create development mysql url
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'mysql+pymysql://root:qushuo@localhost/webapp'
	#set the sqlalchemy_track_modifications key to the false to decrease the memery consumption
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('DEV_TRACK_MODIFICATIONS') or False



class TestingConfig(Config):
	TESTING = True
	#create testing mysql url
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'mysql+pymysql://root:qushuo@localhost/webapp'
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('TEST_TRACK_MODIFICATIONS') or False



class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:qushuo@localhost/webapp'
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('TRACK_MODIFICATIONS') or False




config = {
	'development' : DevelopmentConfig,
	'test' : TestingConfig,
	'production' : ProductionConfig,
	
	'default' : DevelopmentConfig
}