from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

pages = set()
def getLinks(pageUrl):
	global pages
	html = urlopen("http://en.wikipedia.org"+pageUrl)
	bsObj = BeautifulSoup(html)
	for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
		if 'href' in link.attrs:
			# Here is a new page
			newPage = link.attrs['href']
			print(newPage)
			pages.add(newPage)
			time.sleep(5)
			getLinks(newPage)
getLinks(" ") 