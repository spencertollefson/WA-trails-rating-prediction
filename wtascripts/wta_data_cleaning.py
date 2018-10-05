
# coding: utf-8

# # TODO:
# - Clean (see other notebook)
# - Create "distance from Seattle" feature

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as st
# import pymc3 as pm
import seaborn as sns

# enables inline plots, without it plots don't show up in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
# %config InlineBackend.figure_format = 'png'
# mpl.rcParams['figure.dpi']= 300


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 25)
pd.set_option('display.precision', 3)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


# In[3]:


import pickle
def load_pd_pkl(file):
    import pandas as pd
    try:
        with open(f"{file}.pkl",'rb') as picklefile:
            return pickle.load(picklefile)
    except FileNotFoundError:
        df = pd.read_csv(f"{file}.csv")
        with open(f"{file}.pkl", 'wb') as picklefile:
            pickle.dump(df, picklefile)
        return df


# In[4]:


df = load_pd_pkl('data/raw_wta_df')


# In[5]:


#df.to_csv('data/raw_wta_df.csv')


# In[6]:


df.shape


# In[7]:


df.reset_index(drop=True, inplace=True)


# In[8]:


#rename columns
df['votes'] = df['votes'].astype(int)
df['countreports'] = df['countreports'].astype(int)
df['rating'] = df['rating'].astype(float)
df['length'] = df['length'].astype(float)
df['gain'] = df['gain'].astype(float)
df['hpoint'] = df['hpoint'].astype(float)
df['lat'] = df['lat'].astype(float)
df['long'] = df['long'].astype(float)
df.info()


# In[9]:


# Clean hikes which faultily have the 'hpoint' assigned to the "length" to NaN
df.loc[df['length'] == df['hpoint'], 'length'] = np.nan


# In[10]:


# Good! All length types exist with a length preceding it.
df[df['length'].notna() & df['length'].isna()]


# In[11]:


# Accurately update length type of "of" to "miles_of_trails" like on website
df[df.lengthtype == "of"]
df.loc[df['lengthtype'] == "of", 'lengthtype'] = "miles_of_trails"

# Clean hikes which faultily have the 'gain assigned to the "length" to NaN
df.loc[df['length'] == df['gain'], 'length'] = np.nan
df[df.length == df.gain].shape

# rename author1 and author2
df.rename(columns={'author1': 'org_author', "author2":"author"},inplace=True)

# do some renaming of dfs and create new one dropping a few columns and all NaNs
old_df = df.copy()
df = df.drop(columns=['trailhead2','org_author', 'author'])
df.dropna(inplace=True)

# drop hikes without any votes and ratings remaining
df = df.loc[df['votes'] != 0, :]


# In[12]:


# There are 7 passes, and also none and n/a
df.fee.unique()


# In[13]:


##### consider limitations on extreme values in length and gain at this point


# In[14]:


##### should I require votes to be above a certain threshold? 1-5?


# In[115]:


df.describe()


# # Assumptions and changes to data on first pass:
# * Must have 3 votes are greater
# * Remove "one-way" hikes
# * Remove extreme continuous variables (length, high-point, elevation gain)

# In[ ]:


Run below (commented out) tweaks to make tweaks


# In[153]:


# df = df[df.votes > 3].count() # Remove hikes with 3 or less votes contributing to rating
# df = df[df.length > 30] # Remove hikes greater than 30 miles
# df = df[df.gain > 6000] # Remove hikes greater than 6000 feet in vertical gain


# # To-Do
# * Feature engineer lat/long
# * Change and/or remove one-way and miles of trails locations.

# In[156]:


# import pickle

# with open('data/cleaned_wta_df.pkl', 'wb') as picklefile:
#     pickle.dump(df, picklefile)

