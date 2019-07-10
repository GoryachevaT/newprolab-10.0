#!/opt/anaconda/envs/bd9/bin/python3

import sys
import os
import numpy as np
import pandas as pd
import pickle
import re
import json
import xgboost as xgb
from urllib.parse import urlparse, unquote
from pandas.io.json import json_normalize
from sklearn.feature_extraction.text import CountVectorizer  #TfidfVectorizer
#from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
#from sklearn.ensemble import RandomForestClassifier

def main():
    # read data from standard input
    columns=['gender','age','uid','user_json']
    df = pd.read_table(sys.stdin, sep='\t', header=None, names=columns)

    # deserialize json and normalize one level
    df['visits'] = json_normalize(df.user_json.apply(json.loads))
    
    # extract domains and make them words
    df['domains'] = df['visits'].apply(lambda x: [url2domain(item['url']) + "/" + \
                                                    str(pd.Timestamp(item['timestamp'], unit='ms').hour) for item in x])
    df['domains'] = df['domains'].apply(lambda x:' '.join(x))
    
    # drop needless columns
    df.drop(['user_json', 'visits'], axis=1, inplace=True)
    
    # split train and test data
    train_df = df.query("~(gender=='-' & age=='-')")
    test_df = df.query("gender=='-' & age=='-'")
    
    # get count of words in test data from vocabulary (threshold for test data filter)
    test_df['count'] = test_df.domains.apply(lambda x: len([domain for domain in x.split()])) #if domain in vocabulary]))
    t = test_df['count'].median()

    #считать модель из файла в переменную vectorizer
    # predict gender  
    model_file_gender = "project1/project01_model_gender.pickle"
    p1 = pickle.load(open(model_file_gender, 'rb'))
    test_df.loc[test_df['count']>=t, 'gender'] = p1.predict(test_df.loc[test_df['count']>=t, 'domains'])
    # predict age
    model_file_age = "project1/project01_model_age.pickle"
    p2 = pickle.load(open(model_file_age, 'rb'))
    test_df.loc[test_df['count']>=t, 'age'] = p2.predict(test_df.loc[test_df['count']>=t, 'domains'])

    # вывод
    output = test_df.loc[:, ['uid', 'gender', 'age']]
    output.sort_values(by='uid', axis=0, ascending=True, inplace=True)
    sys.stdout.write(output.to_json(orient='records'))


def url2domain(url):
    ''' Extract domains from urls
    '''
    url = re.sub('(http(s)*://)+', 'http://', url)
    parsed_url = urlparse(unquote(url.strip()))
    if parsed_url.scheme not in ['http','https']:
        return None
    netloc = re.search("(?:www\.)?(.*)", parsed_url.netloc).group(1)
    path = re.findall("([a-z]+[a-z0-9]+)", parsed_url.path)
    query = re.findall("([a-z]+[a-z0-9]+)", parsed_url.query)
    if path is not None:
        path = " ".join(path)  #path.group()
        result = netloc + "/" + path
    else:
        result = netloc
    if query is not None:
        query = " ".join(query)
        result = result + "?" + query
    if result is not None:
        return result    #str(result.encode('utf8')).strip()
    return None


def clean_text(text, stop_words):
    '''input - string of domains
       output - string of words with len(word)>=2
    '''
    _split = re.compile(r'([^\w]|[_])').split
    words = [x for x in _split(text)]   # split string into words
    words = [re.sub(r'\d|^x\w+$', '', x) for x in words]
    return " ".join([x for x in words if len(x)>2 and x not in stop_words])


if __name__ == "__main__":
    main()

