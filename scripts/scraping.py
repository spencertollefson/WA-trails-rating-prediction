'''This file contains functions that scrape data from a wta.org
webpage and stores all the data into a row in a pandas DataFrame.'''


######
# Helper Function
######

def get_soup_hike_stat(soup, stat):
    obj = soup.find(text=re.compile(stat))
    if not obj:
        return None
    else:
        return obj

######
# Data Scraping and Retrieval Functions
######

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

######
# DataFrame Functions
######

def append_features(soup, headers):
    '''
    soup: beautifulsoup object of web page
    headers: list of names of the particular wta.org trail page features we want.
    '''
    data = defaultdict()
    for i in headers:
        try:
            # allows to call methods by inserting a string into the func name
            data[i] = [globals()["get_" + i](soup)]
        except:
            data[i] = np.nan
    return data

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