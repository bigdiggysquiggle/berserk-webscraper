#!/usr/bin/env python3

import os
import sys
import requests
import berserk_dl
from bs4 import BeautifulSoup

def get_range(chapters, chapset):
	for i in range(0, len(chapters)):
		while chapters[i].td.text != "Berserk Chapter " + chapset[1].upper():
			i += 1
		while chapters[i].td.text != "Berserk Chapter " + chapset[0].upper():
			if os.path.exists(chapters[i].td.text):
				print("Error: " + chapters[i].td.text + " already exists")
				i += 1
			chap = chapters[i].td.text
			print(chap)
			berserk_dl.dl_chap(chapters[i], chap)
			berserk_dl.make_pdf(chap, "")
			i += 1
		if os.path.exists(chapters[i].td.text):
			print("Error: " + chapters[i].td.text + " already exists")
			continue
		chap = chapters[i].td.text
		print(chap)
		berserk_dl.dl_chap(chapters[i], chap)
		berserk_dl.make_pdf(chap, "")
		break

def get_chaps(chapters, chapset):
	for chapter in chapters:
		if not chapset or not chapset[0]:
			break
		for i in range(0, len(chapset)):
			if chapter.td.text == "Berserk Chapter " + chapset[i].upper():
				if os.path.exists(chapter.td.text):
					print("Error: " + chapter.td.text + " already exists")
					continue
				chap = chapter.td.text
				print(chap)
				berserk_dl.dl_chap(chapter, chap)
				berserk_dl.make_pdf(chap, "")
				chapset = chapset[0:i] + chapset[i+1:]
				break

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Usage: specific_chaps.py [-r <lower number> <higher number>] | [chapter list]")
		exit()
	chapset = []
	r = False
	if sys.argv[1] == '-r':
		if len(sys.argv) != 4:
			print("Error: -r takes exactly 2 arguments")
		else:
			r = True
			chapset = sys.argv[2:]
	else:
		chapset = sys.argv[1:]
	for i in range(0, len(chapset)):
		if chapset[i].isnumeric():
			while len(chapset[i]) < 3:
				chapset[i] = '0' + chapset[i]
	if os.path.exists('output') == False:
		os.mkdir('output')
	os.chdir('output')
	if os.path.exists('jpeg') == False:
		os.mkdir('jpeg')
	if os.path.exists('pdf') == False:
		os.mkdir('pdf')
	os.chdir('jpeg')
	page = requests.get("https://readberserk.com")
	soup = BeautifulSoup(page.text, 'html.parser')
	chapters = soup.select('#content > div > div.col-md-8 > div.card.card-table > div.card-body.table-responsive.p-0 > table > tbody')
	chapters = chapters[0].find_all('tr')
	if r == True:
		get_range(chapters, chapset)
	else:
		get_chaps(chapters, chapset)
