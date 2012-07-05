from flask_peewee.utils import get_object_or_404, object_list

from flask import request, render_template, flash, redirect, url_for
from app import app
from models import Image, Imageuri, ImageFragment, Metadata, Annotation
<<<<<<< HEAD
import exiftool
from imagecontroller import Imagecontroller

imgc = Imagecontroller()
ns_foaf = 'http://xmlns.com/foaf/0.1/'
=======
from imagecontroller import Imagecontroller

imgc = Imagecontroller()
ns_foaf = "http://xmlns.com/foaf/0.1/"
ns_ma = "http://www.w3.org/ns/ma-ont#"
>>>>>>> origin/#1-extend-semantic-annotation

@app.route('/')
def index():

    """
        user is being redirected to the image_timeline
        if the index site is requested
    """
    
    return image_timeline()
    
@app.route('/images/')
def image_timeline():

    """
        function that is called when the url for images
        is being requested
    """
    images = Image.select().order_by(('id', 'asc'))
    return object_list('images.html', images, 'image_list')
    
@app.route('/images/<imageid>/')
def image_detail(imageid):

    """
        function that is when a specific image is requested
        the metadata of the requested image is loaded (if there is one)
        and given to the template
    """

    try: 
        image = Image.get(id=imageid)
        imgfrag = ImageFragment.get(image=image, x=0, y=0, visible=True)
        imgmeta = Metadata.get(imgfrag=imgfrag, namespace="http://www.w3.org/ns/ma-ont#")
        annos = Annotation.get(imgmeta=imgmeta)
        return render_template('image_detail.html', img=image,imgmeta=imgmeta)
    except Imageuri.DoesNotExist:
        flash('Die Bildnummer wurde nicht gefunden. Bitte waehle ein anderes Bild.', 'error')
        return render_template('images.html')
    except ImageFragment.DoesNotExist:
        return render_template('image_detail.html', img=image)

@app.route('/images/<imageid>/addfragment', methods=['GET', 'POST'])
def addfragment(imageid, *context):
<<<<<<< HEAD
=======

    """
        if HTTP verb is POST a new fragment is saved for a specific imageid
        the annotation being saved depends on the type of annotation
        in the frontend in these steps:
        - create imagefragment
        - create metadata for the fragment
        - create annotation for the fragment depending on annotation type
            (everything not is not identified by a specific context of the frontend,
            is being annotated using key-value pairs)
        if HTTP verb is GET the user is being redirected to the image 
        
        ***TODO***
        the typ of annotation data should not depend on the frontend to enable
        using this trough the API --> further improvement needed!
    """

>>>>>>> origin/#1-extend-semantic-annotation
    image = get_object_or_404(Image, id=imageid)

    if request.method == 'POST' and request.form['xvalue']:
        imgfrag = imgc.add_fragment(image, [request.form['xvalue'], request.form['yvalue']])
<<<<<<< HEAD
        if request.args.get('context', 'person'):
            fragmeta = imgc.add_metadata(imgfrag, ns_foaf)
            imgc.add_annotation(fragmeta, 'firstName', request.form['firstName'])
            imgc.add_annotation(fragmeta, 'lastName', request.form['lastName'])
=======
        namespace = request.args.get('namespace')
        fragmeta = imgc.add_metadata(imgfrag, namespace)
        
        if request.args.get('context') == "person":
            imgc.add_annotation(fragmeta, 'name', request.form['name'])
            imgc.add_annotation(fragmeta, 'homepage', request.form['homepage'])
        elif request.args.get('context') == "location":
            imgc.add_annotation(fragmeta, 'locationName', request.form['locationName'])
        elif (request.args.get('context') == "relation") or (request.args.get('context') == "media"):
            imgc.add_annotation(fragmeta, 'relation', request.form['relation'])
        else:
            annokey = request.form['key']
            value = request.form['value']
            imgc.add_annotation(fragmeta, annokey, value)
        
>>>>>>> origin/#1-extend-semantic-annotation
        flash('Das Fragment wurde erfolgreich angelegt!')
        return redirect(url_for('image_detail', imageid=imageid))
    return render_template('image_detail.html', img=image)
    
@app.route('/images/<imageid>/adduri', methods=['GET', 'POST'])
def adduri(imageid):

    """
        if HTTP verb is POST a new fragment is saved for a specific imageid
        the annotation being saved depends on the type of annotation
        in the frontend
        
        ***TODO***
        the typ of annotation data should not depend on the frontend to enable
        using this trough the API --> further improvement needed!
    """
    
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
<<<<<<< HEAD
=======

    """
        if HTTP verb is POST the system checks, if the URI is already in the system
        if YES, the user is being redirected to the image
        if NOT, the image size is checked (for development, image width has to be < 680px)
        if it is allowed, the image is being saved as object, metadata gets extracted
        and the user is being redirected to the image page
        
        ***TODO***
        - check if url is for an image!
        --> Bad Request if not
    """
    
>>>>>>> origin/#1-extend-semantic-annotation
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