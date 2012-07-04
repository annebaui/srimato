import datetime
from flask import request, redirect
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin, ModelAdmin

from app import app, db
from models import Image, Imageuri, ImageFragment, Metadata, Annotation

# create an Auth object for use with our flask app and database wrapper
auth = Auth(app, db)

class ImageAdmin(ModelAdmin):
    columns = ('id','width', 'created',)

class ImageuriAdmin(ModelAdmin):
    columns = ('image','uri', 'created',)	

admin = Admin(app, auth)
admin.register(Image, ImageAdmin)
admin.register(Imageuri, ImageuriAdmin)
admin.register(ImageFragment)
admin.register(Metadata)
admin.register(Annotation)
auth.register_admin(admin)
admin.setup()

auth.User.create_table(fail_silently=True)