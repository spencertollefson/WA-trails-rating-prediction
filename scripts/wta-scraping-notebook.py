'''
Author: Spencer Tollefson
Date: October 4, 2018
Description: This script scrapes all hikes in the WTA.org website for 31
possible characteristics and saves to a pandas DF.

Instructions: Toggle variable READY to True and execute file. Look at
writing df to disk at end of file if interested.
'''

READY = False

from __future__ import print_function, division
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

firefoxdriver = "/usr/local/bin/geckodriver" # path to the chromedriver executable
os.environ["webdriver.firefox.driver"] = firefoxdriver

get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'png' # ‘png’, ‘retina’, ‘jpeg’, ‘svg’, ‘pdf’")

get_ipython().run_line_magic('matplotlib', 'inline')
mpl.rcParams['figure.dpi']= 300

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 25)
pd.set_option('display.precision', 3)

headers = [
    'name',
    'region',
    'subregion',
    'votes',
    'rating',
    'length',
    'lengthtype',
    'gain',
    'hpoint',
    'fee',
    'lat',
    'long',
    'trailhead1',
    'trailhead2',
    'author1',
    'author2',
    'countreports',
          ]

binary_headers = [
    'Wildflowers/Meadows',
    'Ridges/passes',
    'Wildlife',
    'Waterfalls',
    'Old growth',
    'Summits',
    'Good for kids',
    'Dogs allowed on leash',
    'Fall foliage',
    'Lakes',
    'Rivers',
    'Coast',
    'Mountain views',
    'Established campsites',
]

# # Helper Functions

# In[16]:


def get_soup_hike_stat(soup, stat):
    obj = soup.find(text=re.compile(stat))
    if not obj:
        return None
    else:
        return obj


# # Retrieval Functions

# In[17]:


def get_name(soup):
    return soup.find(class_='documentFirstHeading').text

def get_region(soup):
    regions = get_soup_hike_stat(soup, 'Location').find_next().text
    regions = regions.split(sep="--")
    return regions[0].strip()

def get_subregion(soup):
    regions = get_soup_hike_stat(soup, 'Location').find_next().text
    regions = regions.split(sep="--")
    return regions[1].strip()

def get_length(soup):
    length = get_soup_hike_stat(soup, 'Length').find_next().find('span').text
    return length.split()[0]

def get_lengthtype(soup):
    length = get_soup_hike_stat(soup, 'Length').find_next().find('span').text
    return length.split()[2]

def get_gain(soup):
    return get_soup_hike_stat(soup, 'Gain').find_next().text

def get_hpoint(soup):
    return get_soup_hike_stat(soup, 'Highest Point').find_next().text

def get_fee(soup):
    return get_soup_hike_stat(soup, 'Parking Pass/Entry Fee').find_next().text

def get_lat(soup):
    return get_soup_hike_stat(soup, 'Co-ordinates').find_next().text

def get_long(soup):    
    return get_soup_hike_stat(soup, 'Co-ordinates').find_next().find_next().text

def get_trailhead1(soup):
    obj = soup.find(id='trailhead-details').find_all('p')[1].text
    if "weather" in obj:
        return np.nan
    return obj
def get_trailhead2(soup):
    obj = soup.find(id='trailhead-details').find_all('p')[2].text
    if "weather" in obj:
        return np.nan
    return obj

def get_author1(soup):
    return soup.find(class_='authorship sidebar-section').find('p').find_all('span')[0].text

def get_author2(soup):
    return soup.find(class_='authorship sidebar-section').find('p').find_all('span')[1].text

def get_countreports(soup):
    return soup.find(class_='ReportCount').text

def get_votes(soup):
    return soup.find(class_='rating-count').text.split()[0][1:]

def get_rating(soup):
    return soup.find(class_='current-rating').text.split()[0]


# # Function to mark if certain categorical features are present
# 
# ## Only run this after having created the dictionary for the current webpage

# In[18]:


def append_features(soup, headers):
    '''
    soup: beautifulsoup object of web page
    headers: list of names of the particular wta.org trail page features we want.
    ----
    output is defaultdict
    '''
    feat_dict = defaultdict()
    for i in headers:
        try:
            # allows to call methods by inserting a string into the func name
            feat_dict[i] = [globals()["get_" + i](soup)]
        except:
            feat_dict[i] = np.nan
    return feat_dict

def append_binary_feats(soup, binary_headers, feat_dict):
    '''
    soup: beautifulsoup object of web page
    datadict: this is the dictionary used for each webpage to store the variables.
    Thus this function should be called only after that dict has been created.
    ----
    Product: this outcome appends binary categorical features present as a "1" or "0" to an existing
    dictionary
    '''
    bin_features = binary_headers.copy()
    for i in soup.find_all(class_='feature'):
        label = i.attrs['data-title']
        if label in bin_features:
            feat_dict[label] = 1
            bin_features.remove(label)
    for remainder in bin_features:
        feat_dict[remainder] = 0
    return feat_dict


# # Creating Dictionary

# # Combine into one scrape function

# In[22]:


def scrape_page(soup, headers=headers, binary_headers=binary_headers):
    feat_dict = append_features(soup, headers)
    feat_dict = append_binary_feats(soup, binary_headers, feat_dict)
    # Create pandas DataFrame from dictionary
    df_page = pd.DataFrame.from_dict(feat_dict)
    return df_page


# In[23]:


def concat_to_master(df_page, old_df=None):
    if old_df is not None:
        return pd.concat([old_df, df_page], join='inner')
    else:
        print("only 1 DataFrame present - returning it back to you")
        return df_page


# # Beautiful Soup and Scraping

# In[66]:


new_page_df = None
masterdf = None


# In[ ]:


# loop through url from 0 to 3540, in increments of 30
# End of URL has simple integer that counts upward by 30 on each "Next 30" page of list of trails
# https://www.wta.org/go-outside/hikes/?b_start:int=0

# Must substantiate first row of df

# ### This is it! The following cell creates the WTA df with all the data.
# 
# ### **WARNING!!** Cell will take ~ 1 hour and 9 minutes to execute.

# In[83]:


def scrape_and_create_all_wta():
    '''
    Function scrapes every WTA hike page, concatenates info, and returns Pandas DF.
    WARNING!!! This function takes approximately 1 hours and 9 minutes to run
    '''
    # tripreports url changes by number at end. iterates by 30 - begins at 0, ends at 3540
    df = None
    for i in range(0, 3541, 30): 
        wtaurl = f'https://www.wta.org/go-outside/hikes/?b_start:int={i}'
        wtaresponse = requests.get(wtaurl)
        wta_html = wtaresponse.text
        wta_soup = BeautifulSoup(wta_html, 'lxml')
        for j in wta_soup.find_all(class_='listitem-title'):
            page_url = j['href']
            page_response = requests.get(page_url)
            page_html = page_response.text
            page_soup = BeautifulSoup(page_html, 'lxml')
            new_page_df = scrape_page(page_soup)
            df = concat_to_master(new_page_df, df)
    return df


while READY:
    df = scrape_and_create_all_wta()


##### Pickle to save to drive

#import pickle

# with open('data/raw_wta_df.pkl', 'wb') as picklefile:
#     pickle.dump(dfcopy, picklefile)

