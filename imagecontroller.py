from flask import Flask
import exiftool
import urllib2 as urllib
from PIL import Image as PILImage
import StringIO
import tempfile
from models import Image, Imageuri, ImageFragment, Metadata, Annotation
from datacontroller import DataController 

tempimgname = 'tempimg.jpg'
maximagesize = 680
defaultfragsize = 10
gl_image = None
tempfrag = None
tempmeta = None


"""
    the imagecontroller handles all
    functions on the image like the extraction of metadata,
    the creation of a new image object
"""

# namespace for W3C Ontology for Media Resources
ns_ma = "http://www.w3.org/ns/ma-ont#"

class Imagecontroller(object):

    def create_new_image(self, imguri, imgsize):
        global gl_image
        
        """ Creates a new image instance and queries
            metadata thats already included in the file
            resulting in new fragments, metadata and annotations
        """ 
        
        imageob = Image.create(width=imgsize[0], height=imgsize[1],)
        imageob.save()
        imageuri = Imageuri.create(
            image=imageob,
            uri=imguri,
        )
        imageuri.save()
        
        gl_image = imageob
        self.extract_def_metadata(imguri)
        
        return imageob
    
    def extract_def_metadata(self, uri):
        global gl_image
        global tempmeta
        global ns_ma
        
        """ Extracts selected metadata properties
            that are already included in a jpg file
            following the guidelines from MWG
            and W3C Ontology for Media Resources
            displayed by the W3C Ontology for Media Resources 
        """ 
        
        self.create_temp_img_from_uri(uri)
        
        tempfrag = self.add_fragment(gl_image, [0,0])
        tempmeta = self.add_metadata(tempfrag, ns_ma)
        
        self.set_img_locator(uri)
        self.set_img_title(uri)
        self.set_img_desc(uri)
        self.set_img_date(uri)
        self.set_img_creator(uri)
        self.set_img_copyright(uri)
        self.set_img_location(uri)
        self.set_img_policy(uri)
        self.set_img_relation(uri)     
        
    def set_img_locator(self, uri):       
    
        """ getting image locator info
            which gets referenced by the uri, from which 
            the image has been created
        """ 
        
        key = "identifier"
        self.add_annotation(tempmeta, key, uri)
    
    def set_img_title(self, uri):   

        """ getting image title info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources are used first looking at 
            XMP Tags and than MWG
        """ 
    
        tags = ["XMP-dc:Title", "MWG:ImageDescription"]
        key = "title"
        value = self.set_meta_prop(tags, uri, key)
        
    def set_img_desc(self, uri):    
    
        """ getting image description info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources are used first looking at 
            EXIF Tag, than XMP and IPTC
        """ 
        
        tags = ["EXIF:XPSubject", "XMP-dc:Subject", "IPTC:Caption-Abstract"]
        key = "description"
        self.set_meta_prop(tags, uri, key)
    
    def set_img_date(self, uri):
    
        """ getting image date info
            which following MWG guidelines
        """ 
    
        tags = ["MWG:DateTimeOriginal"]
        key = "date"
        self.set_meta_prop(tags, uri, key)
        
    def set_img_creator(self, uri):
    
        """ getting image creator info
            which following MWG guidelines
        """ 
    
        tags = ["MWG:Creator"]
        key = "creator"
        self.set_meta_prop(tags, uri, key)
        
    def set_img_copyright(self, uri):
    
        """ getting image copyright info
            which following MWG guidelines
        """ 
        
        tags = ["MWG:Copyright"]
        key = "copyright"
        self.set_meta_prop(tags, uri, key)
        
    def set_img_location(self, uri):
        
        """ getting image location info
            which following MWG guidelines
        """ 
    
        tags = ["MWG:Location"]
        key = "location"
        self.set_meta_prop(tags, uri, key)
    
    def set_img_policy(self, uri):
        
        """ getting image policy info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources are used first looking at 
            XMP-rights:Certificate, than XMP-rights:UsageTerms and XMP-rights:WebStatement
        """ 
        
        tags = ["XMP-rights:Certificate", "XMP-rights:UsageTerms", "XMP-rights:WebStatement"]
        key = "policy"
        self.set_meta_prop(tags, uri, key)
    
    def set_img_relation(self, uri):
    
        """ getting image relation info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources looking at 
            XMP-dc:Relation
        """ 
        
        tags = ["XMP-dc:Relation"]
        key = "relation"
        self.set_meta_prop(tags, uri, key)
    
    def set_meta_prop(self, tags, uri, key):
        
        """ function for getting any kind of tag of exiftool
            therefore, an image file is streamed to get a 
            local copy of the image to work with
            ***TODO***
            reading each value from exiftool is slowing down performance
            -> save info once in json format and iterate through the file
            to find the information to speed up image "uploading" process
        """
    
        global tempmeta
        
        with exiftool.ExifTool() as et:
            for tag in tags:
                if et.get_tag(tag, tempimgname) != None:     
                    self.add_annotation(tempmeta, key, et.get_tag(tag, tempimgname))
                    return
        
    def add_fragment(self, image, coordinates):
    
        """ Add a fragment to an image instance requiring
            coordinates with first value as x and second value as y
        """ 
        
        try:
            imgfrag = ImageFragment.get(image=image, x=coordinates[0], y=coordinates[1], visible=True)
            return imgfrag
        except ImageFragment.DoesNotExist:
            imgfrag = ImageFragment.create(
                                    image = image,
                                    x = coordinates[0],
                                    y = coordinates[1],
                                    w = defaultfragsize,
                                    h = defaultfragsize,)
            imgfrag.save()
            return imgfrag
        
    def add_metadata(self, fragment, nasp):
    
        """ Adds metadata to a given fragment 
            with an optional namespace attribute 
        """ 

        try:
            imgmeta = Metadata.get(imgfrag=fragment, namespace=nasp)
            newimgmetaversion = imgmeta.version
            newimgmetaversion = newimgmetaversion + 1
            up_query = Metadata.update(version=newimgmetaversion).where(imgfrag=fragment, namespace=nasp)
            up_query.execute()
            return imgmeta
        except Metadata.DoesNotExist:

            imgmeta = Metadata.create(
                                imgfrag = fragment,
                                version = 1,
                                namespace = nasp,)
            imgmeta.save()
            return imgmeta
        
    def add_annotation(self, metadata, key, value):
    
        """ Adds an Annotation to a Metadata Object
            of one namespace
            if the key is already included the value
            will be updated. if the key is not there, a new annotation
            will be created
        """ 
        
        try: 
            Annotation.get(imgmeta=metadata, an_key=key)
            newimgmetaversion = metadata.version
            newimgmetaversion = newimgmetaversion + 1
            meta_query = metadata.update(version=newimgmetaversion)
            meta_query.execute()
            
            anno_query = Annotation.update(an_value=value).where(imgmeta=metadata, an_key=key)
            anno_query.execute()
            return
        except Annotation.DoesNotExist:
            imganno = Annotation.create(
                                imgmeta = metadata,
                                an_key = key,
                                an_value = value,)
            imganno.save()
            return imganno
            
    def get_fragments(self, image):
        return ImageFragment.select().where(image=image)
        
    def get_metadata(self, imgfrag):
        return Metadata.select().where(imgfrag=imgfrag)
        
    def get_annotation(self, imgmeta):
        return Annotation.select().where(imgmeta=imgmeta)
    
    def add_imageuri(self, uri, image):
        
        """ 
            Adds an Imageuri object to a Image Object
        """ 
    
        global ns_ma
        try:
            imageuri = Imageuri.get(uri=uri)
            if imageuri.image == image:
                return False       
        except Imageuri.DoesNotExist:
            imageuri = Imageuri.create(
                image=image,
                uri=uri,
            )
            imageuri.save()
            try: 
                imagefrag = ImageFragment.get(x=0, y=0, image=image)
                urimeta = self.add_metadata(imagefrag, ns_ma)
                self.add_annotation(urimeta, "relation", uri)
                return True
            except ImageFragment.DoesNotExist:
                return False
            return True
              
    def create_temp_img_from_uri(self, uri): 
        
        """ 
            Create a stream of an image file to work with
            url has to be opened again because the
            req.read() from get_img_size crashes data so that
            it cant be streamed
            ***TODO***
            - File should be created by tempfile.py
        """
        
        fp = open(tempimgname, 'wb')
        req = urllib.urlopen(uri)
        for line in req:
            fp.write(line)
        fp.close()
      
        
    def get_image_size(self, uri):
    
        global req
    
        """
            Return the current size of an image.
        """
            
        req = urllib.urlopen(uri)
        im = PILImage.open(StringIO.StringIO(req.read()))
        return im.size
        
    def check_image_size(self, imgsize):
        
        """ 
            Checks the image size. In the GUI, image
            has one restriction for display suppose:
            width < 680px . otherwise the image is being
            rejected.
        """
        if imgsize[0]<=maximagesize:
            return True
        else:
            return False