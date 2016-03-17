import urllib.request
import urllib.error
from urllib.parse import urlsplit
import re
import json
import csv
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from html.parser import HTMLParser
from bs4 import BeautifulSoup

start_time = time.time()

with open('input_urls.csv', 'r') as f:
    reader = csv.reader(f)
    read_list = list(reader)

url_list = []
for item in read_list:
    if item:
        url_list += item


# Checks a list of input urls if they are well-formed.
# Returns a list of well-formed urls.
def check_malformed_url(urls):
    valid_urls = []
    domain_name_list = []
    url_links = []
    for link in urls:
        try:
            url_content = urllib.request.urlopen(link)
            valid_urls += [url_content.read()]

            domain_name = ((link.split('//', 1))[1].split('.com', 1)[0])
            if 'www.' in domain_name:
                domain_name = domain_name.split('www.', 1)[1]
            domain_name_list += [domain_name]

            url_links += [link]
        except Exception as e:
            print("Invalid link: " + link + " because exception: " + str(e))
            pass
    return valid_urls, domain_name_list, url_links


# Acquires the twitter, facebook, and google handles.
# Uses fuzzywuzzy to fuzzy match the strings for comparison of
# domain and appropriate ID.
# Returns a handle(s) as a list.
def get_twitter_facebook_google_id(url_instance, url_link):

    twitter_base = 'twitter.com/'
    facebook_base = 'facebook.com/'
    google_base = 'play.google.com/store/apps/details?'
    request = url_instance
    links = re.findall('"((http|ftp)s?://.*?)"', str(request))
    twitter_IDs = []
    facebook_IDs = []
    google_IDs = []
    if len(links) == 0:
        return twitter_IDs, facebook_IDs, google_IDs
    for link in links:
        link = link[0]
        if twitter_base in link:
            twitter_IDs += [link]
        elif facebook_base in link:
            facebook_IDs += [link]
        elif google_base in link:
            google_IDs += [link]

    twitter_IDs = [link.split('.com/', 1)[1] for link in twitter_IDs]
    twitter_return = [ID for ID in twitter_IDs if
                      fuzz.ratio(ID, url_link) > 75]

    facebook_IDs = [link.split('.com/', 1)[1] for link in facebook_IDs]
    facebook_return = [ID for ID in facebook_IDs if
                       fuzz.ratio(ID, url_link) > 75]

    google_IDs = [link.split('.com/store/apps/details?', 1)[1]
                  for link in google_IDs]
    google_return = [ID for ID in google_IDs]

    return twitter_return, facebook_return, google_return


# Acquires the apple ID through meta content.
def get_apple_id(url_instance):
    try:
        website_html = url_instance
        soup = BeautifulSoup(website_html, "html.parser")
        meta = soup.find("meta", {"name": "apple-itunes-app"})['content']
        if 'app-id=' in meta:
            ID = meta.split('app-id=', 1)[1]
            return [ID]
    except:
        return None


# Processes given input and returns -1 if input is invalid.
def process_output(inp):
    if (inp is None):
        return -1
    elif (len(inp) == 0):
        return -1
    else:
        if (len(inp) > 1):
            return str(inp[0])
        else:
            return str(inp[0])


url_content, domain_name_list, url_links = check_malformed_url(url_list)
main_output = []
start_time = time.time()
count = -1
for url in url_content:
    count += 1
    try:
        apple = get_apple_id(url)
        twitter, facebook, google = get_twitter_facebook_google_id(url, domain_name_list[count])
        key = ["ios", "google", "facebook", "twitter"]
        result = [apple, google, facebook, twitter]
        result = [process_output(inp) for inp in result]
        adjusted_key = []
        for index in range(4):
            if (result[index] != -1):
                adjusted_key += [key[index]]

        result = [val for val in result if val != -1]

        dictionary = dict(zip(adjusted_key, result))
        if (dictionary):
            main_output += [dictionary]
        
    except Exception as e:
        print("Exception: " + str(e) + " " + str(count))
        pass


with open('result.json', 'w') as fp:
    json.dump(main_output, fp, sort_keys=True, indent=4)

end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))