# program to go through indeed search results and call clean_html() on each to get a set of the words in the description of the job
# input: keywords to input into search bar, city & state optional
# output: number of times each word appears printed from most common to least

from bs4 import BeautifulSoup
from time import sleep
from collections import Counter
import requests
import re
import csv
import datetime

#sos_scraping is the package for this project
import sos_scraping as sos

city = input("Input city to search: ")
state = input("Input state to search (Washington = WA): ")
search_words= input("Input search words (software+engineer): ")

# used to determine if a link is a job listing
def job_bool(job):
    if 'clk' in job: 
        if not 'page' in job:
            return job

base_url = 'http://www.indeed.com'   

# Join search paramaters to construct url
final_url_paramters = ['http://www.indeed.com/jobs?q=', search_words, '&l=', city,'%2C+', state]
final_url = ''.join(final_url_paramters)

# get soup object of initial page
init_soup = sos.get_soup(final_url)

# get total number of jobs from search count object
searchCount = str(init_soup.find(id = 'searchCount'))
searchCount = re.findall('\d+', searchCount)

if len(searchCount) > 3:
    total_jobs = (int(searchCount[2])*1000) + int(searchCount[3])
else:
    total_jobs = int(searchCount[2])

print ('Found ',total_jobs,' results with this search.')

total_jobs_int = int(total_jobs)

# indeed returns 10 job listings per page
num_pages = (total_jobs_int)//10

# initializing list to hold job descriptions
job_descriptions = []
keywords_all = []
print("num_pages: ", num_pages)

# loop to drive through all of the search result pages
for i in range(1, num_pages): 
    print ('Getting page', i)
    start_num = str(i) 
    current_page = ''.join([final_url, '&start=', start_num])
    page_obj = sos.get_soup(current_page)

    # the job listings are only in the center collumn so we only iterate through there
    job_link_area = page_obj.find(id = 'resultsCol')
    all_urls = [base_url + link.get('href') for link in job_link_area.find_all('a')]
 
    #job_URLS = filter(lambda x:'clk' in x, job_URLS)
    # using python generator expressions
    job_urls = [url for url in all_urls if job_bool(url)]

    # now grab the text from each listing with our other function.
    for j in range(0, len(job_urls)):
        final_description = sos.clean_html(job_urls[j])
        if final_description: # Only append if clean_html was succesful
                job_descriptions.append(final_description)

    for k in job_descriptions:
        keywords_all.extend(k)
        
num_jobDesc = len(job_descriptions)

print ('Finished collecting descriptions.')
print ('Number of job descriptions found: ', num_jobDesc)

# count how many times a word shows up in all of the job listings.
keyword_count = Counter(keywords_all).most_common()
keyword_set = set(keywords_all)
keyword_fieldnames = ("keyword", "count")

with open("5_2.csv", mode='w', newline= '') as csv_file:
    keyword_writer = csv.writer(csv_file, dialect='excel')
    keyword_writer.writerow(keyword_fieldnames)
    for pair in keyword_count:
        keyword_writer.writerow([pair[0], pair[1]])

print("CSV done.")