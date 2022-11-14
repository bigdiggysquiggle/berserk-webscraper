#!/usr/bin/env python3

import os
import re
import shutil
import img2pdf
import requests
import berserk_dl
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger

def dl_chap(chapter):
	name = chapter.text
	chapter=BeautifulSoup(requests.get(chapter.a['href']).text, 'html.parser')
	pages=chapter.find_all('img')
	if len(pages) == 1:
		return
	os.mkdir(name)
	os.chdir(name)
	i=1
	for page in pages:
		url=page.get('src')
		if url[-1] != 'g':
			url=url[:-1]
		data=requests.get(url)
		with open(str(i) + '.jpeg', 'wb') as file:
			for chunk in data.iter_content(100000):
				file.write(chunk)
		i+=1

def make_pdf(name):
	def to_num(s):
		return int(s.split('.')[0])
	li=os.listdir()
	li.sort(key=to_num)
	imgs=[]
	for fname in li:
		if not fname.endswith(".jpeg"):
			continue
		path=os.getcwd() + "/" + fname
		if os.path.isdir(path):
			continue
		imgs.append(path)
	if not len(imgs):
		return
	file=name + ".pdf"
	with open(file, "wb") as fi:
		fi.write(img2pdf.convert(imgs))
	shutil.move(file, os.getcwd().split("jpeg")[0] +  "pdf/" + name)

if __name__ == '__main__':
	berserk_dl.setup_dirs("Blame")
	page=requests.get("https://blame-manga.com")
	soup=BeautifulSoup(page.text, 'html.parser')
	print("got site")
	chapters=soup.select('#ceo_latest_comics_widget-3 > ul:nth-child(2)')[0].find_all('li')
	for chapter in chapters:
		chap = chapter.text
		print(chap)
		dl_chap(chapter)
		berserk_dl.make_pdf(chap, chap)
