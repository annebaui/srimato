from flask_peewee.utils import get_object_or_404, object_list

import urllib2 as urllib
from PIL import Image as PILImage
import StringIO
from flask import request, render_template, flash, redirect, url_for
from app import app
from models import Image, Imageuri, ImageFragment, Metadata, Annotation
import exiftool
from imagecontroller import Imagecontroller

imgc = Imagecontroller()
ns_foaf = 'http://xmlns.com/foaf/0.1/'

@app.route('/')
def index():
    return image_timeline()
    
@app.route('/images/')
def image_timeline():
    images = Image.select().order_by(('id', 'asc'))
    return object_list('images.html', images, 'image_list')
    
@app.route('/images/<imageid>/')
def image_detail(imageid):
    image = get_object_or_404(Image, id=imageid)
    return render_template('image_detail.html', img=image)

@app.route('/images/<imageid>/addfragment', methods=['GET', 'POST'])
def addfragment(imageid, *context):
    image = get_object_or_404(Image, id=imageid)

    if request.method == 'POST' and request.form['xvalue']:
        imgfrag = imgc.add_fragment(image, [request.form['xvalue'], request.form['yvalue']])
        if request.args.get('context', 'person'):
            fragmeta = imgc.add_metadata(imgfrag, ns_foaf)
            imgc.add_annotation(fragmeta, 'firstName', request.form['firstName'])
            imgc.add_annotation(fragmeta, 'lastName', request.form['lastName'])
        flash('Das Fragment wurde erfolgreich angelegt!')
        return redirect(url_for('image_detail', imageid=imageid))
    return render_template('image_detail.html', img=image)
    
@app.route('/images/<imageid>/adduri', methods=['GET', 'POST'])
def adduri(imageid):
    image = get_object_or_404(Image, id=imageid)
    if request.method == 'POST' and request.form['imguri']:
        if imgc.add_imageuri(request.form['imguri'], image) == True:
            flash('Die URI wurde erfolgreich hinzugefuegt.')
            return redirect(url_for('image_detail', imageid=imageid))
        else: 
            flash('Diese URI existiert bereits fuer dieses Bild - bitte waehle eine andere.', 'error')
            return redirect(url_for('image_detail', imageid=imageid))
    return render_template('image_detail.html', img=image)
    
# ---
# --- Checks if an uri is already in the system - if it is, 
# --- the user is being redirected to the belonging image
# ---
@app.route('/addimage/', methods=['GET', 'POST'])
def addimage():
    if request.method == 'POST' and request.form['imageuri']:
        try:
            imageuri = Imageuri.get(uri=request.form['imageuri'])
            imageob = imageuri.image
            flash('Dieses Bild ist bereits im System gespeichert. Bitte waehle eine andere URI.', 'error')
            return redirect(url_for('image_detail', imageid=imageob.id))
        except Imageuri.DoesNotExist:
            if imgc.check_image_size(request.form['imageuri']) == True:
                imageob = imgc.create_new_image(request.form['imageuri'])                
                flash('Dein Bild wurde erfolgreich ans System uebertragen. Starte nun mit deinen Annotationen.')
                return redirect(url_for('image_detail', imageid=imageob.id))
            else:
                flash('Dieses Bild ist zu gross. Bitte waehle ein Bild, dass maximal 680px breit ist!', 'error')
                return redirect(url_for('addimage'))
    return render_template('addimage.html')