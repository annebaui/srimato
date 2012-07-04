#all the imports
from __future__ import with_statement
import sqlite3, os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from PIL import Image
import urllib2 as urllib
import exiftool

from contextlib import closing

# ----------------------#
# ---- configuration ---#
# ----------------------#
DATABASE = 'C:/dev/flask/srimato/srimato/srimato.db'
DEBUG = True #set to false in production system
SECRET_KEY = 'developement key' # to keep client-side sessions secure - hard to guess, complex!
USERNAME = 'admin'
PASSWORD = 'default'

# ----------------------#
# - create application -#
# ----------------------#

app  = Flask(__name__)

# from_object will look at the given object and then looks for all uppercase variables defined there
# from_envar('FLASKR_SETTINGS', silent=True) will look at a different file!, silent = not to complain if its missing
app.config.from_object(__name__)

#method to connect to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
			
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()		
			
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/addimage', methods=['GET', 'POST'])
def addimage():
	if request.method == 'POST':
		url = request.form['imageuri']
		img_guid = generate_guid()
		
		img = g.db.execute('''insert into image (width, height) values (?, ?)''',[getWidth(url), getHeight(url)])
		g.db.commit()
		flash('Bild wurde erfolgreich ans System ubertragen')
		return render_template('getimage.html', url=url)
	return render_template('addimage.html')
	
@app.route('/getimage')
def getimage():
	images = query_db('select * from image')
	return render_template('getimage.html', images=images)

def query_db(query, args=(), one=False):
	"""Queries the database and returns a list of dictionaries."""
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value)
		for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv	
	
def generate_guid():
	return

def getWidth(url):
	#fd = urllib.urlopen(url)
	#im = Image.open(fd)
	return 300

def getHeight(url):
	#fd = urllib.urlopen(url)
	#im = Image.open(fd)
	return 200
	
def dump_db():
 con = connect_db()
 with open("C:/dev/flask/srimato/srimato/dump.sql", "w") as f:
  for line in con.iterdump():
   f.write("%s\n" % line)
   
files = ["a.jpg", "b.jpg"]
with exiftool.ExifTool() as et:
        #metadata = et.get_metadata_batch(files)
        metadata = et.get_tag("MWG:Description", "a.jpg")
        print metadata
"""for d in metadata:
    print("{:20.20} {:20.20}".format(d["SourceFile"],
                                     d["EXIF:DateTimeOriginal"]))"""
	
# method to fire up the server if the file should run as a standalone application
if __name__ == '__main__':
	app.run()
