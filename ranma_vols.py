#!/usr/bin/env python3

import os
import re
import shutil
from PyPDF2 import PdfMerger

vol_list = [ 17, 36, 58, 80, 102, 124, 146, 168, 190, 212, 234, 256, 278, 300, 322, 344, 366, 388, 407 ]

def make_vol(volstr):
	def to_num(s):
		return int(re.split(r"\D+", s)[-2])
	print("Making " + volstr)
	pwd = os.getcwd()
	os.chdir(pwd.replace("jpeg", "pdf"))
	chapdfs = os.listdir()
	chapdfs.sort(key=to_num)
	merger=PdfMerger(strict=False)
	for each in chapdfs:
		merger.append(each)
	merger.write(volstr + ".pdf")
	merger.close()
	os.chdir("../")
	print("Complete")

def move_chaps(start, stop, num):
	os.mkdir("Volume " + str(num))
	while (start <= stop):
		try:
			shutil.move("Ranma 1_2 Chapter " + str(start), "Ranma 1_2 - Volume " + str(num))
		except:
			shutil.move("Ranma 1_2 Chapter " + str(start) + ".pdf", "Ranma 1_2 - Volume " + str(num))
		start += 1

if __name__ == '__main__':
	i = 1
	vol = 0
	os.chdir("Ranma 1_2/pdf")
	print("opening directory")
	while vol < len(vol_list):
		print("moving Volume " + str(vol + 1) + " pdf")
		move_chaps(i, vol_list[vol], vol + 1)
		os.chdir("../jpeg")
		print("moving Volume " + str(vol + 1) + " jpeg")
		move_chaps(i, vol_list[vol], vol + 1)
		print("making Volume")
		os.chdir("Volume " + str(vol + 1))
		make_vol("Volume " + str(vol + 1))
		i = vol_list[vol] + 1
		vol += 1
