# getInternalLinks.py
# Defines a function to get the internal links of a web page.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getInternalLinks(bsObj, includeURL)