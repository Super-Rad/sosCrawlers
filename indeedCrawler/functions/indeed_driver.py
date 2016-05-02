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

# need to change input to be keywords later
def crawl_indeed(city = None, state = None):

    city = "Seattle"
    state = "WA"
    
    base_url = 'html://www.indeed.com' 

    #indeed sees this as "software engineer" typed into keyword search bar
    search_words = 'software+engineer'  

    # Join search paramaters to construct url
    final_url = ['http://www.indeed.com/jobs?q=%22', search_words, '%22&l=', city,'%2C+', state]

    # try to open our search
    try:
        html = urllib.request.urlopen(final_url).read()
    except:
           print ('Something went wrong when opening initial url')
    return
    init_soup = BeautifulSoup(html)

    # get total number of jobs from search count object
    num_jobs_area = init_soup.find(id = 'searchCount').string.encode('utf-8')

    # extract the number from the object, this returns each digit as an array, we reconstruct into a single into a single number
    job_numbers = re.findall('\d+', num_jobs_area)
    if len(job_numbers) > 3: 
        total_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
    else:
        total_jobs = int(job_numbers[2]) 

    print ('Found ',total_jobs,' results with your search.')

    # indeed returns 10 job listings per page
    num_pages = total_num_jobs/10

    # initializing list to hold job descriptions
    job_descriptions = []

    # loop to drive through all of the search result pages
    for i in xrange(1,num_pages+1): 
            print ('Getting page', i)
            start_num = str(i*10) 
            current_page = ''.join([final_url, '&start=', start_num])
            
    html_page = urllib.request.urlopen(current_page).read()
    page_obj = BeautifulSoup(html_page)

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

    csv_name = "4/18/2016"

    keyword_dict = Counter(doc_frequency)
    keyword_fieldnames = [keyword, count]
    keyword_writer = csv.DictWriter(csv_name, fieldnames = keyword_fieldnames)

    keyword_writer.writeheader()
    keyword_writer.writerows()

    return csv_name