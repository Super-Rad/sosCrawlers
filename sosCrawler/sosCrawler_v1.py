# Zack Startzman
# sosCrawler_v1.py
# A web crawler made to map the sos syllabus page for project websites

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

pages = set()
startPage = "http://ada.evergreen.edu/sos/proj16w/projects16w.html"

def getLinks(pageUrl=startPage):
	global pages
	html = urlopen(pageUrl)
	bsObj = BeautifulSoup(html)
	for link in bsObj.findAll("a"):
		if 'href' in link.attrs:
			# Here is a new page
			newPage = link.attrs['href']
			print(newPage)
			pages.add(newPage)
			getLinks(newPage)
getLinks()