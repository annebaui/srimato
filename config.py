# config

class Configuration(object):
    DATABASE = {
        'name': 'srimato.db',
        'engine': 'peewee.SqliteDatabase',
    }
    DEBUG = True
	#SECRET_KEY has to be changed in production mode
    SECRET_KEY = 'developement key'
