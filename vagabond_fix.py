#!/usr/bin/env python3

import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import ranma1_2

if __name__ == '__main__':
	output = "Vagabond"
	link = "https://preview.comick.fun/comic/vagabond/zgZ0O-chapter-null-en"
	options = Options()
	print("starting firefox")
	driver = webdriver.Firefox(options=options, service_log_path='/dev/null')
	driver.get(link)
	time.sleep(5)
	print("got site")
	chap_num = 15
	os.chdir(output + "/jpeg")
	for m in range(500):
		driver.execute_script("window.scrollBy(0, 1080)")
		time.sleep(0.25)
	chapname = output + " Volume " + str(chap_num)
	print("getting " + chapname)
	ranma1_2.chap_dl(driver=driver, name=chapname)
	ranma1_2.make_pdf(chapname)
