from bs4 import BeautifulSoup
import urllib2
import re

def clean_html(website):
	
	# check if website is valid
	try:
		site = urllib2.urlopen(website).read()
	except:
		return

	site_soup = BeautifulSoup(site)

	# remove script and style tags from object
	for script in soup_obj (["script","style"]):
		script.extract()

	# get text from object
	text = site_soup.get_text()

	lines = (line.strip() for line in text.splitlines())
	
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

	# puts spaces between chunks
	def chunk_space(chunk):
		chunk_out = chunk + ' '
		return chunk_out

	# more chunk formatting removes blank lines and end of lines
	text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8')

	# try to get unicode, some websites don't less me do it this way. Hence the try.
	try:
		text = text.decode('unicode_escape').encode('ascii','ignore')
	except:
		return

	# regex, need + for c++
	text = re.sub("[^a-zA-z.+"," ", text)

	#return only the set
	text = list(set(text))

	return text