# config

"""
        Sets up the database configuration 
        using a sqlite database
        ***TODO***
        in production mode change:
        > SECRET_KEY to one that is hard to guess
        > DEBUG to False
"""

class Configuration(object):
    DATABASE = {
        'name': 'srimato.db',
        'engine': 'peewee.SqliteDatabase',
    }
    DEBUG = True
    SECRET_KEY = 'developement key'