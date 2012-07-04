# - srimato


a semantic region-based image annotation tool that 

main functions:

* awareness of available metadata of a jpeg file deployed following the W3C Ontology for Media Resources following the rules of MWG
* getting and editing metadata of JPEG File of any URL ( currently JPEG with max. width of 680px )
* getting metadata in HTML, RDF/XML or JSON
* saving metatdata in back to JPEG File


requirements:

* `flask <https://github.com/mitsuhiko/flask>`_

* `peewee <https://github.com/coleifer/peewee>`_
* `PIL - Python Imaging Library <http://www.pythonware.com/products/pil/>`_
* python 2.7

* `PyExifTool - A Python wrapper for Phil Harvey’s ExifTool <https://github.com/smarnach/pyexiftool>`_
	--> needs an installation of Phil Harvey ExifTool <http://www.sno.phy.queensu.ca/~phil/exiftool/>
	--> under windows: put exiftool.exe into the windows directory (e.g. C:\Windows)



If everything is installed, launch runserver.py
