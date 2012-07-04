from flask import Flask

# flask-peewee bindings
from flask_peewee.db import Database

app = Flask(__name__)
app.config.from_object('config.Configuration')

# instantiate the db wrapper - connects to the database on each request and close it when finished
db = Database(app)

def create_tables():
    from models import Image, Imageuri, ImageFragment, Metadata, Annotation
    Image.create_table()
    Imageuri.create_table()
    ImageFragment.create_table()
    Metadata.create_table()
    Annotation.create_table()


