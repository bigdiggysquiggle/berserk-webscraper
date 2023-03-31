#!/usr/bin/env python3

import os
import re
import time
import shutil
import img2pdf
import requests
import berserk_dl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from PyPDF2 import PdfMerger

def make_vols(start, end, vol_list, name):
	os.chdir(name)
	while start <= end:
		vol = start
		i = 1 if vol == 0 else vol_list[vol - 1] + 1
		volstr = "Volume " + str(vol)
		os.chdir("jpeg")
		move_chaps(i, vol_list[vol], volstr, name)
		os.chdir("../pdf")
		move_chaps(i, vol_list[vol], volstr, name)
		os.chdir(volstr)
		make_vol(volstr)
		os.chdir("../../")

def make_vol(volstr):
	def to_num(s):
		return int(re.split(r"\D+", s)[-2])
	chapdfs = os.listdir()
	chapdfs.sort(key=to_num)
	merger = PdfMerger(strict=False)
	for each in chapdfs:
		merger.append(each)
	merger.write(volstr + ".pdf")
	merger.close()

def move_chaps(start, stop, volstr, name):
	os.mkdir(volstr)
	while start <= stop:
		try:
			shutil.move(name + " Chapter " + str(start), volstr)
		except:
			shutil.move(name + " Chapter " + str(start) + ".pdf", volstr)
		start += 1

def make_pdf(directory):
	def to_num(s):
		return int(s.split('.')[0])
	listed = os.listdir()
	listed.sort(key=to_num)
	imgs = []
	for fname in listed:
		if not fname.endswith(".png"):
			continue
		path = os.getcwd() + "/" + fname
		if os.path.isdir(path):
			continue
		imgs.append(path)
	if not len(imgs):
		return
	file = directory + ".pdf"
	with open(file, "wb") as f:
		f.write(img2pdf.convert(imgs))
	shutil.move(file, os.getcwd().split("jpeg")[0] + "pdf/")
	os.chdir("..")

def chap_dl(driver, name, regex=r"comick.pictures"):
	elements = driver.find_elements(By.TAG_NAME, "img")
	i = 0
	os.mkdir(name)
	os.chdir(name)
	for element in elements:
		try:
			url = element.get_attribute('src')
			if not re.search(regex, url):
				continue
			if i == 0:
				i += 1
				continue
			data = requests.get(url)
			with open(str(i) + ".png", "wb") as file:
				for chunk in data.iter_content(100000):
					file.write(chunk)
			print("got page " + str(i))
			i += 1
		except:
			continue

#TODO: find a way to determine we've hit the end of the page
def scrape(output, link, start, end, load_range=100):
	berserk_dl.setup_dirs(output)
	options = Options()
	print("starting firefox")
	driver = webdriver.Firefox(options=options, service_log_path='/dev/null')
	driver.get(link)
	time.sleep(5)
	print("got site")
	chap_num = start
	if (start != end):
		next_button = driver.find_element(By.XPATH, "//*[text()='Next']")
	print("loading full page")
	while chap_num <= end:
		for m in range(load_range):
			driver.execute_script("window.scrollBy(0, 1080)")
			time.sleep(0.25)
		if start != end and chap_num > 1:
			next_button = driver.find_element(By.XPATH, "//*[text()='Next']")
		chapname = output + " Volume " + str(chap_num)
		print("getting " + chapname)
		chap_dl(driver=driver, name=chapname)
		make_pdf(chapname)
		if start != end:
			next_button.click()
		chap_num += 1
	driver.quit()
