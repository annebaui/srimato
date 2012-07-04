from flask_peewee.utils import get_object_or_404, object_list

import urllib2 as urllib
from PIL import Image as PILImage
import StringIO
from flask import request, render_template, flash, redirect, url_for
from app import app
from models import Image, Imageuri, ImageFragment, Metadata, Annotation

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
def addfragment(imageid):
    image = get_object_or_404(Image, id=imageid)
    defaultfragsize = 10
    if request.method == 'POST' and request.form['xvalue']:
        imgfrag = ImageFragment.create(
                                image = image,
                                x = request.form['xvalue'],
                                y = request.form['yvalue'],
                                w = defaultfragsize,
                                h = defaultfragsize,)
        imgfrag.save()
        flash('Das Fragment wurde erfolgreich angelegt!')
        return redirect(url_for('image_detail', imageid=imageid))
    return render_template('image_detail.html', img=image)
    
@app.route('/images/<imageid>/adduri', methods=['GET', 'POST'])
def adduri(imageid):
    image = get_object_or_404(Image, id=imageid)
    if request.method == 'POST' and request.form['imguri']:
        try:
            imageuri = Imageuri.get(uri=request.form['imguri'])
            if imageuri.image == image:
                flash('Diese URI existiert bereits fuer dieses Bild - bitte waehle eine andere.', 'error')
                return redirect(url_for('image_detail', imageid=imageid))
        except Imageuri.DoesNotExist:
            imageuri = Imageuri.create(
                image=image,
                uri=request.form['imguri'],
            )
            imageuri.save()
            flash('Die URI wurde erfolgreich hinzugefuegt.')
            return redirect(url_for('image_detail', imageid=imageid))
    return render_template('image_detail.html', img=image)
    
# ---
# --- Checks if an uri is already in the system - if it is, 
# --- the user is being redirected to the belonging image
# ---
@app.route('/addimage/', methods=['GET', 'POST'])
def addimage():
    maximagesize = 680
    if request.method == 'POST' and request.form['imageuri']:
        try:
            imageuri = Imageuri.get(uri=request.form['imageuri'])
            imageob = imageuri.image
            flash('Dieses Bild ist bereits im System gespeichert. Bitte waehle eine andere URI.', 'error')
            return redirect(url_for('image_detail', imageid=imageob.id))
        except Imageuri.DoesNotExist:
            fp = urllib.urlopen(request.form['imageuri'])
            im = PILImage.open(StringIO.StringIO(fp.read()))
             
            if im.size[0] <= maximagesize:
                imageob = Image.create(width=200, height=200,)
                imageob.save()
                imageuri = Imageuri.create(
                    image=imageob,
                    uri=request.form['imageuri'],
                )
                imageuri.save()
                flash('Dein Bild wurde erfolgreich ans System uebertragen. Starte nun mit deinen Annotationen.')
                return redirect(url_for('image_detail', imageid=imageob.id))
            else:
                flash('Dieses Bild ist zu gross. Bitte waehle ein Bild, dass maximal 680px breit ist!', 'error')
                return redirect(url_for('addimage'))
    return render_template('addimage.html')