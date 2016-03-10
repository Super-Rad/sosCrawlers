# wikicrawler.py

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
	html = urlopen("http://www.indeed.com/jobs?q=software+engineer&l=Seattle%2C+WA")
	bsObj = BeautifulSoup(html)
	jobList = bsObj.findAll(("a", href=re.compile("^(/rc/)")):
		for link in jobList.attrs:
			print(jobList.get_text())
				print(len(jobList))