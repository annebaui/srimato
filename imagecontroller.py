from flask import Flask
import exiftool
import urllib2 as urllib
from PIL import Image as PILImage
import StringIO
from models import Image, Imageuri, ImageFragment, Metadata, Annotation

tempimgname = 'tempimg.jpg'
maximagesize = 680
defaultfragsize = 10
gl_image = None
tempfrag = None
tempmeta = None

# namespace for W3C Ontology for Media Resources
ns_ma = "http://www.w3.org/ns/ma-ont#"

class Imagecontroller(object):

    def create_new_image(self, imguri):
        global gl_image
        
        """ Creates a new image instance and queries
            metadata thats already included in the file
            resulting in new fragments, metadata and annotations
        """ 
        
        imageob = Image.create(width=self.get_image_size(imguri)[0], height=self.get_image_size(imguri)[1],)
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
        
        tempfrag = self.add_fragment(gl_image, [0,0])
        tempmeta = self.add_metadata(tempfrag, ns_ma)
        
<<<<<<< HEAD
        self.get_img_locator(uri)
        self.get_img_title(uri)
        self.get_img_desc(uri)
        self.get_img_date(uri)
        self.get_img_creator(uri)
        self.get_img_copyright(uri)
        self.get_img_location(uri)
        self.get_img_policy(uri)
        self.get_img_relation(uri)
        self.get_img_relation(uri)
        
    def get_img_locator(self, uri):       
=======
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
>>>>>>> origin/#1-extend-semantic-annotation
    
        """ getting image locator info
            which gets referenced by the uri, from which 
            the image has been created
        """ 
        
        key = "identifier"
        self.add_annotation(tempmeta, key, uri)
    
<<<<<<< HEAD
    def get_img_title(self, uri):   
=======
    def set_img_title(self, uri):   
>>>>>>> origin/#1-extend-semantic-annotation

        """ getting image title info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources are used first looking at 
            XMP Tags and than MWG
        """ 
    
        tags = ["XMP-dc:Title", "MWG:ImageDescription"]
        key = "title"
<<<<<<< HEAD
        value = self.get_meta_prop(tags, uri, key)
        
    def get_img_desc(self, uri):    
=======
        value = self.set_meta_prop(tags, uri, key)
        
    def set_img_desc(self, uri):    
>>>>>>> origin/#1-extend-semantic-annotation
    
        """ getting image description info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources are used first looking at 
            EXIF Tag, than XMP and IPTC
        """ 
        
        tags = ["EXIF:XPSubject", "XMP-dc:Subject", "IPTC:Caption-Abstract"]
        key = "description"
<<<<<<< HEAD
        self.get_meta_prop(tags, uri, key)
    
    def get_img_date(self, uri):
=======
        self.set_meta_prop(tags, uri, key)
    
    def set_img_date(self, uri):
>>>>>>> origin/#1-extend-semantic-annotation
    
        """ getting image date info
            which following MWG guidelines
        """ 
    
        tags = ["MWG:DateTimeOriginal"]
        key = "date"
<<<<<<< HEAD
        self.get_meta_prop(tags, uri, key)
        
    def get_img_creator(self, uri):
=======
        self.set_meta_prop(tags, uri, key)
        
    def set_img_creator(self, uri):
>>>>>>> origin/#1-extend-semantic-annotation
    
        """ getting image creator info
            which following MWG guidelines
        """ 
    
        tags = ["MWG:Creator"]
        key = "creator"
<<<<<<< HEAD
        self.get_meta_prop(tags, uri, key)
        
    def get_img_copyright(self, uri):
=======
        self.set_meta_prop(tags, uri, key)
        
    def set_img_copyright(self, uri):
>>>>>>> origin/#1-extend-semantic-annotation
    
        """ getting image copyright info
            which following MWG guidelines
        """ 
        
        tags = ["MWG:Copyright"]
        key = "copyright"
<<<<<<< HEAD
        self.get_meta_prop(tags, uri, key)
        
    def get_img_location(self, uri):
=======
        self.set_meta_prop(tags, uri, key)
        
    def set_img_location(self, uri):
>>>>>>> origin/#1-extend-semantic-annotation
        
        """ getting image location info
            which following MWG guidelines
        """ 
    
        tags = ["MWG:Location"]
        key = "location"
<<<<<<< HEAD
        self.get_meta_prop(tags, uri, key)
    
    def get_img_policy(self, uri):
=======
        self.set_meta_prop(tags, uri, key)
    
    def set_img_policy(self, uri):
>>>>>>> origin/#1-extend-semantic-annotation
        
        """ getting image policy info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources are used first looking at 
            XMP-rights:Certificate, than XMP-rights:UsageTerms and XMP-rights:WebStatement
        """ 
        
        tags = ["XMP-rights:Certificate", "XMP-rights:UsageTerms", "XMP-rights:WebStatement"]
        key = "policy"
<<<<<<< HEAD
        self.get_meta_prop(tags, uri, key)
    
    def get_img_relation(self, uri):
=======
        self.set_meta_prop(tags, uri, key)
    
    def set_img_relation(self, uri):
>>>>>>> origin/#1-extend-semantic-annotation
    
        """ getting image relation info
            which has no MWG guidelines - therefor, the mapping rules from
            W3C Ontology for Media Resources looking at 
            XMP-dc:Relation
        """ 
        
        tags = ["XMP-dc:Relation"]
        key = "relation"
<<<<<<< HEAD
        self.get_meta_prop(tags, uri, key)
    
    def get_meta_prop(self, tags, uri, key):
=======
        self.set_meta_prop(tags, uri, key)
    
    def set_meta_prop(self, tags, uri, key):
>>>>>>> origin/#1-extend-semantic-annotation
        
        """ function for getting any kind of tag of exiftool
            therefore, an image file is streamed to get a 
            local copy of the image to work with
            ***TODO***
            reading each value from exiftool is slowing down performance
            -> save info once in json format and iterate through the file
            to find the information to speed up image "uploading" process
        """
    
        global tempmeta
        
        self.create_temp_img_from_uri(uri)
        with exiftool.ExifTool() as et:
            for tag in tags:
                if et.get_tag(tag, tempimgname) != None:     
                    self.add_annotation(tempmeta, key, et.get_tag(tag, tempimgname))
                    return
        
    def add_fragment(self, image, coordinates):
    
        """ Add a fragment to an image instance requiring
            coordinates with first value as x and second value as y
        """ 
        
<<<<<<< HEAD
        imgfrag = ImageFragment.create(
                                image = image,
                                x = coordinates[0],
                                y = coordinates[1],
                                w = defaultfragsize,
                                h = defaultfragsize,)
        imgfrag.save()
        return imgfrag
=======
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
>>>>>>> origin/#1-extend-semantic-annotation
        
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
<<<<<<< HEAD
        """ 
        
        imganno = Annotation.create(
                            imgmeta = metadata,
                            an_key = key,
                            an_value = value,)
        imganno.save()
        return imganno
=======
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
>>>>>>> origin/#1-extend-semantic-annotation
    
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
        """
        
        fp = open(tempimgname, 'wb')
        req = urllib.urlopen(uri)
        for line in req:
            fp.write(line)
        fp.close()
        
    def get_image_size(self, uri):
    
        """ 
            Gets a current size of an image.
        """
            
        fp = urllib.urlopen(uri)
        im = PILImage.open(StringIO.StringIO(fp.read()))
        return im.size
        
    def check_image_size(self, uri):
        
        """ 
            Checks the image size. In the GUI, image
            has one restriction for display suppose:
            width < 680px . otherwise the image is being
            rejected.
        """
    
        fp = urllib.urlopen(uri)
        im = PILImage.open(StringIO.StringIO(fp.read()))
        if im.size[0]<=maximagesize:
            return True
        else:
            return False