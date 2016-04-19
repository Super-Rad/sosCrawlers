from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html)

nameList = bsObj.findAll("span", {"class":"green"})
princeList = bsObj.findAll(text = "the prince")

for name in nameList:
	print(name.get_text())
print(len(princeList))