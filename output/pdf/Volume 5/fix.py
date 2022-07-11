#!/usr/bin/env python3

import os
from PyPDF2 import PdfFileMerger

name = "Volume 5.pdf"
li = [ "O0", "P0", "001", "002", "003", "004", "005", "006"]
merger = PdfFileMerger(strict=False)
for each in li:
	merger.append("Berserk Chapter " + each + ".pdf")
merger.write("Volume 5.pdf")
merger.close()
