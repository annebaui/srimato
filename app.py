from flask import Flask

from flask_peewee.db import Database

app = Flask(__name__)
app.config.from_object('config.Configuration')

# instantiate db wrapper - handles connection to the database on each request and close it when finished
db = Database(app)

def create_tables():
    from models import Image, Imageuri, ImageFragment, Metadata, Annotation
    Image.create_table()
    Imageuri.create_table()
    ImageFragment.create_table()
    Metadata.create_table()
    Annotation.create_table()


