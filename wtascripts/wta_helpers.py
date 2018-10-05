'''
Helper scripts for WTA project
Author: Spencer Tollefson
Date: October 5, 2018
'''

def clean_raw_df(df, minvotes=False, maxlength=False, maxgain=False, excludeoneway=False):
    """Clean WTA dataframe to be model ready.
    Keyword arguments:
    df -- the raw df scraped (see wta_scraping_notebook.py to scrape it)
    minvotes -- (int) min. number of votes toward rating a hike may have to be included
    maxlength -- (int) max. length of hike (mi.) a hike may have to be included 
    maxgain -- (int) max. vertical gain (ft.) a hike may have to be included
    oneway -- (bool) True if one-way labeled hikes should be included
    """
    import pandas as pd
    import numpy as np

    # Set index and change column datatypes
    df.reset_index(drop=True, inplace=True)
    df['votes'] = df['votes'].astype(int)
    df['countreports'] = df['countreports'].astype(int)
    df['rating'] = df['rating'].astype(float)
    df['length'] = df['length'].astype(float)
    df['gain'] = df['gain'].astype(float)
    df['hpoint'] = df['hpoint'].astype(float)
    df['lat'] = df['lat'].astype(float)
    df['long'] = df['long'].astype(float)

    # Clean hikes which faultily have the 'hpoint' assigned to the "length" to NaN
    df.loc[df['length'] == df['hpoint'], 'length'] = np.nan

    # Accurately update length type of "of" to "miles_of_trails" like on website
    df.loc[df['lengthtype'] == "of", 'lengthtype'] = "miles_of_trails"

    # Clean hikes which faultily have the 'gain assigned to the "length" to NaN
    df.loc[df['length'] == df['gain'], 'length'] = np.nan

    # rename author1 and author2
    df.rename(columns={'author1': 'org_author', "author2":"author"},inplace=True)

    # Drop a few columns and all NaNs
    df = df.drop(columns=['trailhead2','org_author', 'author'])
    df.dropna(inplace=True)

    # drop hikes without any votes and ratings remaining
    df = df.loc[df['votes'] != 0, :]

    if minvotes is not False:
        df = df[df.votes >= minvotes] # Remove hikes with X or less votes contributing to rating

    if maxlength is not False:
        df = df[df.length < maxlength] # Remove hikes greater than X miles

    if maxgain is not False:
        df = df[df.gain < maxgain] # Remove hikes greater than 6000 feet in vertical gain

    if excludeoneway is True:
        df = df[df.lengthtype != "one-way"] # Remove hikes measured as "one-way"
    return df
    