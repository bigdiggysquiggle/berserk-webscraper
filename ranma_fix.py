#!/usr/bin/env python3

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import ranma1_2

if __name__ == '__main__':
	try:
		chap_num = int(sys.argv[1])
	except:
		print("input must be a number between 1 and 407")
	output = "Ranma 1_2"
	link = "https://preview.comick.fun/comic/ranma-1-2/4w9Vk-chapter-407-en"
	options = Options()
	print("starting firefox")
	driver = webdriver.Firefox(options=options, service_log_path='/dev/null')
	driver.get(link)
	time.sleep(5)
	print("got site")
	chap_num = 407
	os.chdir(output + "/jpeg")
	for m in range(100):
		driver.execute_script("window.scrollBy(0, 1080)")
		time.sleep(0.5)
	chapname = output + " Chapter " + str(chap_num)
	print("getting " + chapname)
	ranma1_2.chap_dl(driver=driver, name=chapname)
	ranma1_2.make_pdf(chapname)
