#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

import pandas as pd

def get_something_from_source(something0,source, something1):
    r = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{something0}/{source}/property/{something1}/JSON').json()
    return r['PropertyTable']['Properties'][0][something1]

