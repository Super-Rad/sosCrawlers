from urllib.request import urlopen
html = urlopen("http://www.facebook.com")
print(html.read())