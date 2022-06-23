#!/usr/bin/env python3

import berserk_dl
import os
import requests
from bs4 import BeautifulSoup

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
for chapter in chapters:
	chap = chapter.td.text
	print(chap)
	berserk_dl.dl_chap(chapter)
	berserk_dl.make_pdf(chap, "")
