from app import app, db

from api import api
from admin import admin
from models import *
from views import *

admin.setup()
api.setup()

if __name__ == '__main__':
  app.run()
