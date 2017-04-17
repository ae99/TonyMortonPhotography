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

def populate(input):
	ide,name,description,original,file = input[0],input[1],input[2],input[3],input[4]

	if Photo.objects.filter(id = ide).count() == 0:
		p = Photo(id=ide, name=name, description=description, original=original)
	
	
		url = "http://tonymortonphotography.com/thumbnail/thumb" + file
		try:
			p.source.save(file, File(urllib.request.urlopen(url)))
		except:
			print("FAILED FAILED FAILED, item", ide, name )

		print('Populated', name)

if __name__ == '__main__':
	print("Queuing")
	with open('data.csv') as f:
		reader = csv.DictReader(f)
		a = 1000
		photos = []
		for row in reader:
			a += 17
			ide = hex(a)[2:]
			photos.append([ide,row['name'],row['description'],row['original'],row['file']]) 

		print("Populating")
		pool = ThreadPool(32)

		# for i in photos:
		# 	populate(i)

		results = pool.map(populate, photos)
		pool.close()
		pool.join()


