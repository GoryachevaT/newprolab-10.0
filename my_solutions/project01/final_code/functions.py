import pandas as pd
import datetime
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

dict_gender_to_gendercategory = {'M':1,'F':0,'-':-1}
dict_age_to_agecategory = {'18-24':0,'25-34':1,'35-44':2,'45-54':3,'>=55':4,'-':-1}

dict_gendercategory_to_gender = {True:'M',False:'F'}
dict_agecategory_to_age = {0: '18-24', 1: '25-34', 2: '35-44', 3: '45-54', 4: '>=55'}

def load_user_json(user_jsons: pd.Series) -> pd.Series:
	'''apply ~.map(json.loads)~ to pd.Series'''
	import json
	return user_jsons.map(json.loads)

def url2domain(url:str) -> str:
    '''return domain of the given url'''
    import re
    from urllib.parse import urlparse
    from urllib.request import urlretrieve, unquote
    url = re.sub('(http(s)*://)+', 'http://', url)
    parsed_url = urlparse(unquote(url.strip()))
    if parsed_url.scheme not in ['http','https']: 
        return None
    netloc = re.search("(?:www\.)?(.*)", parsed_url.netloc).group(1)
    if netloc is not None: 
        return str(netloc.encode('utf8')).strip()
    return None

def load_data():
    df = pd.read_csv('/data/share/project01/gender_age_dataset.txt', sep='\t')
    mask_test = df['gender']=='-'
    return df[mask_test].reset_index(drop = True), df[~mask_test].reset_index(drop = True)

def make_harmonic_features(value, period=24):
    value *= 2 * np.pi / period
    return np.cos(value), np.sin(value)

def get_time(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp/1000).hour

def get_mode(values):
    if len(set(values))>1:
        kernel = stats.gaussian_kde(values)
        height = kernel.pdf(values)
        return values[np.argmax(height)]
    elif len(set(values))==0:
        return values[0]
    else:
        return 0