# All functions used to get information from indeed
from bs4 import BeautifulSoup
import requests
import re

def get_soup(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
    
    print("Connecting to: ", url)
    
    requested = requests.get(url, headers=headers, allow_redirects=True)
    
    print("Got: ", requested.url)
    
    html = requested.text
    soup = BeautifulSoup(html, "html.parser")
    
    return soup

# function to clean the html from and return a set of words
# from a beautifulsoup object
def clean_html(website):
    site_soup = get_soup(website)

    # remove script and style tags from object
    for script in site_soup (["script","style"]):
        script.extract()

    # get text from object
    text = site_soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # puts spaces between chunks of text
    def chunk_space(chunk):
        chunk_out = chunk + ' '
        return chunk_out

    # more chunk formatting removes blank lines and end of lines
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk)

    # regex, need + for c++
    text = re.sub("[^a-zA-Z.+3]"," ", text)
    text = text.lower().split()

    #return only the set
    text = list(set(text))

    return text
