#!/usr/bin/env python3

import os
import re
import shutil
import img2pdf
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger

# This is the main script. When ran, it will download
# every single panel from every single chapter, condense
# them down into pdfs of each chapter, then further
# condensing those pdfs into volumes. Due to the way the
# last few chapters have been released, I have elected
# to put them in their own volume to both simplify my
# life in writing this script and in actually reading
# those chapters in the future


# As I download the pictures, they get numbered and
# saved as a jpeg. This function takes each of those
# jpegs and compiles them into the aforementioned
# pdf of the chapter. In order to accomplish this,
# we first get the complete list of items in the
# directory, then we sort them by numerical value
# as sorting by string value would put them slightly
# out of order. Every string that starts with a 1
# would end up together instead of counting up in
# a numerically logical fashion. In order to get
# the actual numeric value of the file, we have to
# do something to beable to ignore that pesky file
# extension. Well, because I'm specifically naming
# these files just a number and a file extension,
# we can split at the '.' and only use the file's
# name as an integer
def make_pdf(directory, volstr):
	def to_num(s):
		return int(s.split('.')[0])
	li = os.listdir()
	li.sort(key=to_num)
	imgs = []
	for fname in li:
		if not fname.endswith(".jpeg"):
			continue
		path = os.getcwd() + '/' + fname
		if os.path.isdir(path):
			continue
		imgs.append(path)
	file = directory + ".pdf"
	with open(file,"wb") as f:
		f.write(img2pdf.convert(imgs))
	shutil.move(file, os.getcwd().split("jpeg")[0] + "pdf/" + volstr)
	os.chdir('..')


# Once we have finished downloading and converting each
# chapter of a volume into pdfs, we still want to create
# a big pdf containing the entire volume. PdfFileMerger
# saves the day here, offering what's probably the easiest
# way to use what we've already done up to this point. All
# we have to do is append each chapter to the internal
# list the PdfFileMerger keeps track of, then tell it to
# write them all to a given output file. Then we just
# close the merger and that's that
def make_vol(volstr):
	print("Making " + volstr)
	pwd = os.getcwd()
	os.chdir(pwd.replace("jpeg", "pdf"))
	chapdfs = os.listdir()
	chapdfs.sort()
	merger=PdfFileMerger(strict=False)
	for each in chapdfs:
		merger.append(each)
	merger.write(volstr + ".pdf")
	merger.close()
	merger=PdfFileMerger()
	os.chdir(pwd)

# This was probably the easiest thing I've ever scraped.
# The HTML for every chapter is laid out really clean
# and neat, the url for every panel is consistent (and
# consistently in the same place), and every image I
# don't want to scrape comes from a completely different
# url so it's really easy to regex match which urls I do
# and which urls I don't scrape. The one minor issue I
# ran into is that getting the url from our instance of
# BeautifulSoup sometimes puts a unicode character on
# the end. We just do a quick check to make sure that 
# our url is clean and clean it up if it's not
def dl_chap(chapter):
	os.mkdir(chapter.td.text)
	os.chdir(chapter.td.text)
	chapter=BeautifulSoup(requests.get(chapter.a['href']).text, 'html.parser')
	pages=chapter.find_all('img', {'class': 'pages__img'})
	i = 1
	for page in pages:
		url=page.get('src')
		if not re.search(r"(readberserk|staticflickr)", url):
			continue
		if url[-1] != 'g':
			url=url[:-1]
		data=requests.get(url)
		with open(str(i) + '.jpeg', 'wb') as file:
			for chunk in data.iter_content(100000):
				file.write(chunk)
		i += 1

# This function was originally a stub, but due to the
# fact that I have to correct the last couple entries
# by hand I decided to ultimately leave this here.
def get_vol_list():
	return ['Berserk Chapter A0', 'Berserk Chapter D0', 'Berserk Chapter F0', 'Berserk Chapter J0', 'Berserk Chapter O0', 'Berserk Chapter 007', 'Berserk Chapter 017', 'Berserk Chapter 027', 'Berserk Chapter 037', 'Berserk Chapter 048', 'Berserk Chapter 059', 'Berserk Chapter 070', 'Berserk Chapter 080', 'Berserk Chapter 092', 'Berserk Chapter 100', 'Berserk Chapter 111', 'Berserk Chapter 122', 'Berserk Chapter 133', 'Berserk Chapter 144', 'Berserk Chapter 155', 'Berserk Chapter 166', 'Berserk Chapter 177', 'Berserk Chapter 187', 'Berserk Chapter 197', 'Berserk Chapter 207', 'Berserk Chapter 217', 'Berserk Chapter 227', 'Berserk Chapter 237', 'Berserk Chapter 247', 'Berserk Chapter 257', 'Berserk Chapter 267', 'Berserk Chapter 277', 'Berserk Chapter 287', 'Berserk Chapter 297', 'Berserk Chapter 307', 'Berserk Chapter 316', 'Berserk Chapter 325', 'Berserk Chapter 334', 'Berserk Chapter 343', 'Berserk Chapter 351', 'Berserk Chapter 359', 'Berserk Chapter 364']

# Get our list of chapters that mark the start of each
# volume
volumes = get_vol_list()
# Remove any previous output so that we don't have to
# factor previous output into our logic, then make
# our output directories
if os.path.exists('output'):
	shutil.rmtree('output')
os.mkdir('output')
os.chdir('output')
os.mkdir('jpeg')
os.mkdir('pdf')
os.chdir('jpeg')
# Get our main page, make our soup, and start
# finding our chapters
page=requests.get("https://readberserk.com")
soup=BeautifulSoup(page.text, 'html.parser')
chapters=soup.select('#content > div > div.col-md-8 > div.card.card-table > div.card-body.table-responsive.p-0 > table > tbody')
chapters=chapters[0].find_all('tr')
# -2 accounts for a nonsense entry at the end
# of our volumes list and also drastically
# simplifies our math and our access of the
# actual volumes array. We're scraping from
# the last chapter all the way back to the
# first so the fact that Python offers an
# easy way to access their data structures
# in that same manner is really helpful
i = -2
l = len(volumes)
# Set up our folders to contain the chapters
# that will make up our volumes, then start
# actually aquiring the chapters and
# converting them
volstr = "Volume 42"
os.mkdir(volstr)
os.chdir(volstr)
os.mkdir(os.getcwd().replace("jpeg", "pdf"))
for chapter in chapters:
	chap = chapter.td.text
	print(chap)
	dl_chap(chapter)
	make_pdf(chap, volstr)
	if chap == volumes[i]:
		make_vol(volstr)
		volstr = "Volume " + str(l+i)
		i -= 1
		os.mkdir("../" + volstr)
		os.chdir("../" + volstr)
		os.mkdir(os.getcwd().replace("jpeg", "pdf"))
