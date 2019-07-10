#!/opt/anaconda/envs/bd9/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import os, sys
import json
import pickle
from urllib.parse import urlparse
from urllib.request import urlretrieve, unquote

def url2domain(url):
    url = re.sub('(http(s)*://)+', 'http://', url)
    parsed_url = urlparse(unquote(url.strip()))
    if parsed_url.scheme not in ['http','https']: return None
    netloc = re.search("(?:www\.)?(.*)", parsed_url.netloc).group(1)
    #if netloc is not None: return str(netloc.encode('utf8')).strip()
    if netloc is not None: return str(netloc.strip())
    return None

def get_domains(j):
    return " ".join([url2domain(d['url']) for d in json.loads(j)['visits'] ])

columns=['gender','age','uid','user_json']

df = pd.read_table(
    sys.stdin, 
    sep='\t', 
    header=None, 
    names=columns
)


df['urls'] = df['user_json'].apply(get_domains, 0)

data = df[(df.gender == '-') & (df.age == '-')]

with open('project01_model.pickle', 'rb') as f:
    model = pickle.load( f)

pred = model.predict(data['urls'])
data['gender'] = [s[:1] for s in pred]
data['age'] = [s[1:] for s in pred]

output = data[['uid', 'gender', 'age']]
output.sort_values(by='uid',axis = 0, ascending = True, inplace = True)
sys.stdout.write(output.to_json(orient='records'))