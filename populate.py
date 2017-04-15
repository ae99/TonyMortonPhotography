from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request
import csv
import sys



import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','TMP.settings')

import django
django.setup()
from photos.models import Photo



def populate(id,name,description,original,file,):
	p = Photo(id=ide, name=name, description=description, original=original)
	url = "http://tonymortonphotography.com/uploads/" + file
	
	# img_temp = NamedTemporaryFile(delete=True)
	# img_temp.write(urllib.request.urlopen(url).read())
	# img_temp.flush()

	p.source.save(file, File(urllib.request.urlopen(url)))

	p.save()

import random

if __name__ == '__main__':
	print("Populating")
	with open('data.csv') as f:
		reader = csv.DictReader(f)
		a = 1000
		for row in reader:
			a += random.randint(0,200)
			ide = hex(a)[2:]
			populate(ide,row['name'],row['description'],row['original'],row['file'])
			print('Populated bird', row['name'])

