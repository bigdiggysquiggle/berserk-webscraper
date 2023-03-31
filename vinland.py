#!/usr/bin/env python3

import os
import re
import requests
import berserk_dl
from bs4 import BeautifulSoup

from PIL import Image

def fix_imgs():
	print("Bad images detected. Repaired automatically.")
	def to_num(s):
		return int(s.split('.')[0])
	files = os.listdir()
	files.sort(key=to_num)
	for file in files:
		with Image.open(file) as fixing:
			print(file)
			fixing.save("fixed " + file.split('.')[0] + ".png")
		os.remove(file)
		os.rename("fixed " + file.split('.')[0] + ".png", file)

def dl_chap(chapter, name):
	chapter=BeautifulSoup(requests.get(chapter.a['href']).text, 'html.parser')
	pages=chapter.find_all('img')
	if len(pages) == 1:
		return
	os.mkdir(name)
	os.chdir(name)
	i=1
	for page in pages:
		if name == "Vinland Saga, Chapter 157" and i == 18: #switch to checking the filename instead of the i count
			break
		try:
			url=page.get('src')
			if not re.search(r"hxmanga.com/file|toonix.xyz/cdn_mangaraw", url):
				continue
			if url[-1] != 'g':
				url=url[:-1]
			file = url.split('/')[-1]
			try:
				int(file.split('.')[0])
			except:
				continue
			data=requests.get(url)
			with open(file.split('.')[0] + '.jpeg', 'wb') as file:
				for chunk in data.iter_content(100000):
					file.write(chunk)
			i+=1
		except:
			continue

vols = ['Vinland Saga, Chapter 1', 'Vinland Saga, Chapter 6', 'Vinland Saga, Chapter 17', 'Vinland Saga, Chapter 22', 'Vinland Saga, Chapter 29', 'Vinland Saga, Chapter 36', 'Vinland Saga, Chapter 43', 'Vinland Saga, Chapter 50', 'Vinland Saga, Chapter 57', 'Vinland Saga, Chapter 65', 'Vinland Saga, Chapter 72', 'Vinland Saga, Chapter 79', 'Vinland Saga, Chapter 87', 'Vinland Saga, Chapter 94', 'Vinland Saga, Chapter 101', 'Vinland Saga, Chapter 108', 'Vinland Saga, Chapter 116', 'Vinland Saga, Chapter 123', 'Vinland Saga, Chapter 130', 'Vinland Saga, Chapter 137', 'Vinland Saga, Chapter 145', 'Vinland Saga, Chapter 153', 'Vinland Saga, Chapter 161', 'Vinland Saga, Chapter 167', 'Vinland Saga, Chapter 176', 'Vinland Saga, Chapter 184', 'Vinland Saga, Chapter 192']

if __name__ == '__main__':
	berserk_dl.setup_dirs("Vinland Saga")
	page=requests.get("https://read-vinlandsaga.com/")
	soup=BeautifulSoup(page.text, 'html.parser')
	print("got site")
	#soup sieve couldn't find the expected <ul> because there are 2 of them
	#contained in the parent so I had to manually get the correct one
	chapters=soup.select('#post-7 > div > figure')[0].find_all('ul')[-1].find_all('li')
	chapters=chapters[1:]
	i = -1
	volst = "Volume " + str(len(vols))
	os.mkdir(volst)
	os.chdir(volst)
	os.mkdir(os.getcwd().replace('jpeg', 'pdf'))
	for chapter in chapters:
		#some chapters contain a sub title, gotta filter that out
		chap = "Vinland Saga, Chapter " + chapter.text.strip().split(':')[0].strip().split(' ')[-1]
		print(chap)
		dl_chap(chapter, chap)
		try:
			berserk_dl.make_pdf(chap, volst)
		except:
			fix_imgs()
			berserk_dl.make_pdf(chap, volst)
		if chap == vols[i]:
			berserk_dl.make_vol(volst)
			if volst == "Volume 1": #I don't like having this check here
				exit()
			volst = "Volume " + str(int(volst.split(' ')[1]) - 1)
			i -= 1
			if vols[i] != vols[0]:
				os.mkdir("../" + volst)
				os.chdir("../" + volst)
				os.mkdir(os.getcwd().replace("jpeg", "pdf"))
