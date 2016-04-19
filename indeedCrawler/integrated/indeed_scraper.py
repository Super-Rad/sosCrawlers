# program to go through indeed search results and call clean_html() on each to get a set of the words in the description of the job
# input: keywords to input into search bar, city & state optional
# output: number of times each word appears printed from most common to least

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

# function to get soup object of a url
def get_soup(url):
    try:
        print("Connecting to: ", url)
        html = urllib.request.urlopen(url).read()
    except:
        print ('Something went wrong when opening initial url')
        print ('None will be returned instead')
        html = None
    soup = BeautifulSoup(html)
    return soup

# function to clean the html from and return a set of words in a job description on indeed
def clean_html(website):
    
    site_soup = get_soup(website)

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


# need to change input to be keywords later
#def crawl_indeed(city = None, state = None):

base_url = 'html://www.indeed.com'   

# Join search paramaters to construct url
final_url_paramters = ['http://www.indeed.com/jobs?q=', search_words, '&l=', city,'%2C+', state]
final_url = ''.join(final_url_paramters)

# get soup object of initial page
init_soup = get_soup(final_url)

# get total number of jobs from search count object
searchCount = str(init_soup.find(id = 'searchCount'))
searchCount = re.findall('\d+', searchCount)

if len(searchCount) > 3:
    total_jobs = (int(searchCount[2])*1000) + int(searchCount[3])
else:
    total_jobs = int(searChount[2])

print ('Found ',total_jobs,' results with this search.')

total_jobs_int = int(total_jobs)

# indeed returns 10 job listings per page
num_pages = total_jobs_int/10

# initializing list to hold job descriptions
job_descriptions = []

# loop to drive through all of the search result pages
for i in range(1,num_pages+1): 
        print ('Getting page', i)
        start_num = str(i*10) 
        current_page = ''.join([final_url, '&start=', start_num])
        

page_obj = get_soup(current_page)

# the job listings are only in the center collumn so we only iterate through there
job_link_area = page_obj.find(id = 'resultsCol')

# get all urls and filter using a magic lambda function
job_URLS = [base_url + link.get('href') for link in job_link_area.find_all('a')]
job_URLS = filter(lambda x:'clk' in x, job_URLS)

# now grab the text from each listing with our other function.
for j in xrange(0,len(job_URLS)):
            final_description = clean_html(job_URLS[j])
            if final_description: # Only append if clean_html was succesful
                job_descriptions.append(final_description)
            sleep(1)

num_jobDesc = len(job_descriptions)

print ('Finished collecting descriptions.')
print ('Number of job descriptions succesfully found: ', num_jobDesc)

# now to count how many times a word shows up in all of the job listings.
doc_frequency = Counter()
[doc_frequency.update(item) for item in job_descriptions]

keyword_dict = Counter(doc_frequency)
keyword_fieldnames = [keyword, count]
keyword_writer = csv.DictWriter(csv_name, fieldnames = keyword_fieldnames)

keyword_writer.writeheader()
keyword_writer.writerows()