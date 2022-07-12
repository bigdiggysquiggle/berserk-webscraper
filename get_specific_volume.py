#!/usr/bin/env python3

import os
import sys
import requests
import berserk_dl
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
	print("Usage: get_specific_volume.py")
	exit()
start = int(sys.argv[1])
if 1 > start or start > 41:
	print("Error: must be between 1 and 41")
volset = berserk_dl.get_vol_list()
if os.path.exists("output") == False:
	os.mkdir("output")
os.chdir("output")
if os.path.exists("jpeg") == False:
	os.mkdir("jpeg")
if os.path.exists("pdf") == False:
	os.mkdir("pdf")
os.chdir("jpeg")
if os.path.exists("Volume " + str(start)):
	os.removedirs("Volume " + str(start))
os.mkdir("Volume " + str(start))
os.chdir("Volume " + str(start))
if os.path.exists(os.getcwd().replace("jpeg", "pdf")):
	os.removedirs(os.getcwd().replace("jpeg", "pdf"))
os.mkdir(os.getcwd().replace("jpeg", "pdf"))
page = requests.get("https://readberserk.com")
soup = BeautifulSoup(page.text, 'html.parser')
chapters = soup.select('#content > div > div.col-md-8 > div.card.card-table > div.card-body.table-responsive.p-0 > table > tbody')
chapters = chapters[0].find_all('tr')
i = 0
while chapters[i].td.text != volset[start]:
	i += 1
i += 1
start -= 1
while chapters[i].td.text != volset[start]:
	chapter = chapters[i].td.text
	print(chapter)
	berserk_dl.dl_chap(chapters[i])
	berserk_dl.make_pdf(chapter, "Volume " + str(start + 1))
	i += 1
chapter = chapters[i].td.text
print(chapter)
berserk_dl.dl_chap(chapters[i])
berserk_dl.make_pdf(chapter, "Volume " + str(start + 1))
i += 1
berserk_dl.make_vol("Volume " + str(start + 1))
