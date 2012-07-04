from flask import Flask
import exiftool
import urllib2 as urllib
from PIL import Image as PILImage
import StringIO
from models import Image, Imageuri, ImageFragment, Metadata, Annotation

tempimgname = 'tempimg.jpg'
maximagesize = 680

class Imagecontroller(object):
    def create_new_image(self, imguri):
        imageob = Image.create(width=self.get_image_size(imguri)[0], height=self.get_image_size(imguri)[1],)
        imageob.save()
        imageuri = Imageuri.create(
            image=imageob,
            uri=imguri,
        )
        imageuri.save()
        return imageob

    def extract_metadata(self, uri):
        self.create_temp_img_from_uri(uri)
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata( tempimgname )
            print metadata

    def create_temp_img_from_uri(self, uri): 
        fp = open(tempimgname, 'wb')
        req = urllib.urlopen(uri)
        for line in req:
            fp.write(line)
        fp.close()
        
    def get_image_size(self, uri):
        fp = urllib.urlopen(uri)
        im = PILImage.open(StringIO.StringIO(fp.read()))
        return im.size
        
    def check_image_size(self, uri):
        fp = urllib.urlopen(uri)
        im = PILImage.open(StringIO.StringIO(fp.read()))
        if im.size[0]<=maximagesize:
            return True
        else:
            return False