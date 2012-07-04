import datetime

from peewee import *

from app import db

class Image(db.Model):
    width = IntegerField()
    height = IntegerField()
    created = DateTimeField(default=datetime.datetime.now)
    
    #def __unicode__(self):
       #return self.id
    
    def has_uris(self):
        return Image.select().join(Imageuri, on="has_img_uris").where(image=self).order_by('id')
    
class Imageuri(db.Model):
    uri = CharField()
    image = ForeignKeyField(Image, related_name='imageuris')
    created = DateTimeField(default=datetime.datetime.now) 

class ImageFragment(db.Model):
    image = ForeignKeyField(Image, related_name='imagefrag')
    x = IntegerField()
    y = IntegerField()
    w = IntegerField()
    h = IntegerField()
    visible = BooleanField(default=True)
    
class Metadata(db.Model):
    imgfrag = ForeignKeyField(ImageFragment, related_name='fragmeta')
    version = IntegerField()
    timestamp = DateTimeField(default=datetime.datetime.now) 
    namespace = CharField()
    
class Annotation(db.Model):
    imgmeta = ForeignKeyField(Metadata, related_name='anno')
    an_key = CharField()
    an_value = CharField()
