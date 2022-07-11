#!/usr/bin/env python3

import os
from PyPDF2 import PdfFileMerger

name = "Volume 5.pdf"
li = os.listdir()
li.sort()
li = li[:-1]
tmp = li[-1]
li[-1] = li[-2]
li[-2] = tmp
print(li)
merger = PdfFileMerger(strict=False)
for each in li:
	merger.append(each)
merger.write("Volume 14.pdf")
merger.close()
