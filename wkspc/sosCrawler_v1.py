from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

pages = set()
def getLinks(pageUrl):
	global pages
	startPage = urlopen("http://ada.evergreen.edu/sos/proj16w/projects16w.html")
	bsStart = BeautifulSoup(startPage)
	for link in bsObj.findAll("a"):
		if 'href' in link.attrs:
			# Here is a new page
			newPage = link.attrs['href']
			print(newPage)
			pages.add(newPage)
			getLinks(newPage)
getLinks(" ") 