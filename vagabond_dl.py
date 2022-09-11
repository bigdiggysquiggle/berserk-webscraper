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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

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

if __name__ == '__main__':
	output = "Vagabond"
	link = "https://preview.comick.fun/comic/vagabond/3mW79-chapter-null-en"
	berserk_dl.setup_dirs(output)
	options = Options()
#	options.headless = true
	print("starting firefox")
	driver = webdriver.Firefox(options=options, service_log_path='/dev/null')
	driver.get(link)
	time.sleep(5)
	print("got site")
	chap_num = 1
	#there are 37 volumes of this manga
	next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div/div[2]/a')
	for n in range(37):
		for m in range(500):
			driver.execute_script("window.scrollBy(0, 1080)")
			time.sleep(0.25)
		if chap_num > 1:
			next_button = driver.find_element(By.XPATH, "//*[text()='Next']")
		chapname = output + " Volume " + str(chap_num)
		print("getting " + chapname)
		chap_dl(driver=driver, name=chapname)
		make_pdf(chapname)
		next_button.click()
		chap_num += 1
