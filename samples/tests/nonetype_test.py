from bs4 import BeautifulSoup
from time import sleep
from collections import Counter
import urllib.request
import re
import csv
import datetime

# parameters are currently here
csv_name = "4_18_2016"
city = "Seattle"
state = "WA"
search_words = 'software+engineer'

def get_soup(url):
    try:
        print("Connecting to: ", url)
        html = urllib.request.urlopen(url).read()
    except:
        print ('Something went wrong when opening initial url')
        print ('Google homepage will be returned instead')
        html = urllib.request.urlopen("http://www.google.com/")
    soup = BeautifulSoup(html)
    return soup


final_url = ''.join(['http://www.indeed.com/jobs?q=', search_words, '&l=', city,'%2C+', state])

init_soup = get_soup(final_url)

print (init_soup.title.get_text())
