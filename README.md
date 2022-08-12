Current issues:
- Sometimes Volume 1 gets created twice and a volume 0 gets 
  made

- Volumes 4 and 14 are out of order. I'm implementing temp
  fixes until I can get around to making a better sort
  algorithm

TODO:
- separate out the new set of chapters from the
  currently established volumes

I started this project for a couple reasons. I'm a little
bit of a data hoarder so writing a script that could help
me hoard a little more data is always appealing, one of
my friends showed interest in having pdfs on hand as well,
and I needed anotehr project that would teach me new
skills and libraries I hadn't ever used before

This project makes use of img2pdf as the main driver
behind the actual conversion of images to pdfs (shocker
I know). It was the fastest and most efficient option
available in comparison to the more popular alternatives,
so I elected to install it and use it. It took a little
bit of playing around to really get the hang of using the
library. Admittedly the function that uses it is based on
an example use case from the documentation itself, just
adapted to my specific use case.

Beyond that, I also used PdfFileMerger which trivialized
the last stretch of the project (creating the volumes
from the chapter pdfs) and I used BeautifulSoup.
BeautifulSoup is an incredible library. It offers such
an easy to use set of methods to interact with html.
The only downsides are that it doesn't support finding
elements by xpath and it doesn't support any dynamically
loaded content. If the element you're looking for isn't
present in the base HTML, you're gonna have to use
another tool like Selenium.

If you've stumbled upon this repo, congratulations!
You were smart enough to actually Google whether or
not someone had already done legwork on this niche
project, unlike me who dove headfirst into building
and didn't even think about Googling for a solution
till I was already running the script for the final
time. I learned a lot though and sharpened my Python
skills further so it was definitely not time wasted.

To use this project, just run the berserk_dl.py script
while inside whichever directory you want it to create
the output directories in.

Dependencies:
-img2pdf
-PyPDF2

TODO:
new bug. Something is being stuck together that shouldn't be
