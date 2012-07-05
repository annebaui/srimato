from flask_peewee.rest import RestAPI, RestResource

from app import app
from models import Image, Imageuri, ImageFragment, Metadata, Annotation

# instantiate the api wrapper
api = RestAPI(app)

# Each model is getting a representational RestResource to be
# displayed when querying the API

class ImageResource(RestResource):
    fields = ('width', 'height', 'created', 'id',)
    
class ImageResourceID(RestResource):
    fields = ('id')
    
class ImageuriResource(RestResource):
    include_resources = {'image': ImageResourceID}
    
class ImageFragmentResource(RestResource):
    include_resources = {'image': ImageResourceID}
    
class MetadataResource(RestResource):
    include_resources = {'imgfrag': ImageFragmentResource}
        
class AnnotationResource(RestResource):
    include_resources = {'imgmeta': MetadataResource}

# register our models so they are exposed via /api/<model>/
api.register(Image, ImageResource)
api.register(Imageuri, ImageuriResource)
api.register(ImageFragment, ImageFragmentResource)
api.register(Metadata, MetadataResource)
api.register(Annotation, AnnotationResource)