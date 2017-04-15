from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request
import csv
import sys

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','TMP.settings')

import django
django.setup()
from photos.models import Photo

# import map

def populate(input):
	ide,name,description,original,file = input[0],input[1],input[2],input[3],input[4]

	p = Photo(id=ide, name=name, description=description, original=original)
	url = "http://tonymortonphotography.com/uploads/" + file
	
	# img_temp = NamedTemporaryFile(delete=True)
	# img_temp.write(urllib.request.urlopen(url).read())
	# img_temp.flush()

	p.source.save(file, File(urllib.request.urlopen(url)))
	print('Populated', name, ide)
	# p.save()

import random

if __name__ == '__main__':
	print("Queuing")
	with open('data.csv') as f:
		reader = csv.DictReader(f)
		a = 1000
		photos = []
		for row in reader:
			a += random.randint(0,200)
			ide = hex(a)[2:]
			print(ide)
			photos.append([ide,row['name'],row['description'],row['original'],row['file']]) 

		print("Populating")
		pool = ThreadPool()

		results = pool.map(populate, photos)
		pool.close()
		pool.join()

