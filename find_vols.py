#!/usr/bin/env python3

import os
from PIL import Image

# As the beginning of each volume is signified by having
# a full-colour first image, we can detect and lay out
# where each volume begins by determining which chapters
# have a full colour image as their first image. This
# script originally would have output a "vol.json" file
# that the main script would have used in order to group
# the chapters into appropriate volumes and make full
# volume pdfs out of them. However once I ran it once,
# printed the output, and hardcoded it into 
# berserk_dl.py, I realized this really doesn't need to
# create json data as the json library that Python has
# available drastically trivializes the creation,
# storage, and conversion of json data to the point
# where there's no value in creating a python script
# that uses json data as a means of practice

# Also due to the way the last few chapters were released,
# the method of determining the start of a volume by the
# presence or absence of colour falls apart. But that's
# easy to account for and fix by hand. The vast majority
# of Berserk in the form it's being hosted does conform
# to only using colour for the covers of the volume

# This greyscale detection method was found on stackoverflow:
# https://stackoverflow.com/questions/23660929/how-to-check-whether-a-jpeg-image-is-color-or-gray-scale-using-only-python-stdli
# written by the user joaoricardo000

def is_grey_scale(img_path):
	img = Image.open(img_path).convert('RGB')
	w, h = img.size
	for i in range(w):
		for j in range(h):
			r, g, b = img.getpixel((i,j))
			if r != g != b:
				return False
	return True

def find_volumes(chapters, i, volumes=[]):
	volstr = "Volume "
	for chapter in chapters:
		os.chdir(chapter)
		if not is_grey_scale("1.jpeg"):
			print(volstr + str(i) + ", " + chapter)
			volumes.append(chapter)
			i += 1
		os.chdir("..")
	return i, volumes

if __name__ == 'main':
	os.chdir("./output/jpeg")
	dirs=os.listdir()
	dirs.sort()
# Because Berserk starts with chapter A0 we have to
# either come up with a different sort method, or be
# lazy and split the list into two lists that will get
# processed separately
	dirs1=dirs[365:]
	dirs2=dirs[:365]
	i = 1
	i, volumes = find_volumes(dirs1, i)
	i, volumes = find_volumes(dirs2, i, volumes)
	print(volumes)
