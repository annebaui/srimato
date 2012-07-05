import datetime

from peewee import *

from app import db

"""
    Models just for the relational mapping to the database
    ***TODO***
    identifiers have to get unique ids instead of default
    to ensure interoperabiliy
    1, 2, 3 etc.
"""

class Image(db.Model):
    width = IntegerField()
    height = IntegerField()
    created = DateTimeField(default=datetime.datetime.now)
       
    def has_uris(self):
        return Image.select().join(Imageuri, on="has_img_uris").where(image=self).order_by('id')
    
    def get_key_value(self, meta, key):
        
        try:
            return (Annotation.get(imgmeta=meta, an_key=key)).an_value
        except Annotation.DoesNotExist:
            return
        
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
    
    """
        visible is a reference for deleted - but the fragment stays 
        stored in the database to enable revisions in the future
    """
        
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