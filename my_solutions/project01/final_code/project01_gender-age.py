#!/opt/anaconda/envs/bd9/bin/python

import sys
import pandas as pd
import json
import lightgbm as lgb
import re
from urllib.parse import urlparse
from urllib.request import urlretrieve, unquote
import numpy as np
import pickle
from content_bigdata10_proj1.notebooks.functions import dict_gender_to_gendercategory
from content_bigdata10_proj1.notebooks.functions import dict_gendercategory_to_gender
from content_bigdata10_proj1.notebooks.functions import dict_age_to_agecategory
from content_bigdata10_proj1.notebooks.functions import dict_agecategory_to_age
from content_bigdata10_proj1.notebooks.functions import load_user_json
from content_bigdata10_proj1.notebooks.functions import url2domain
from content_bigdata10_proj1.notebooks.functions import get_time
from content_bigdata10_proj1.notebooks.functions import get_mode
from content_bigdata10_proj1.notebooks.functions import make_harmonic_features


columns=['gender','age','uid','user_json']

df = pd.read_table(
    sys.stdin, 
    sep='\t', 
    header=None, 
    names=columns
)

def feature_engineering(df):
    #user_json - конвертация строки в json
    df['user_json'] = load_user_json(df['user_json'])
    
    #user_json - вычитываем домен
    df['domain_list'] = df['user_json'].map(lambda x: [url2domain(visit['url']) for visit in x['visits']])
    
    #user_json - вычитываем unix время
    df['time_list'] = df['user_json'].map(lambda x: [visit['timestamp'] for visit in x['visits']])
    
    
    #получаем для юзера список времен посечения страницы (число от 0 до 24)
    df['hours'] = [list(map(get_time,time_list)) for time_list in df['time_list']]
    
    #получаем моду времени посещения страницы
    df['hour_mode'] = [get_mode(hour_list) for hour_list in df['hours']]
    
    #конвертация моды в косинус
    df['hours_harmonics_cos'] = [make_harmonic_features(time_list)[0] for time_list in df['hour_mode']]
    
    #конвертация моды в синус
    df['hours_harmonics_sin'] = [make_harmonic_features(time_list)[1] for time_list in df['hour_mode']]
    
    #количество визитов
    df['visits'] = df['time_list'].apply(len)
    
    #логарифмируем количество визитов
    df['visits'] = np.log1p(df['visits'])
    
    #время между первым и последним посещением
    df['time_range'] = df['time_list'].apply(np.ptp)
    
    #среднее время на посещение
    df['visit_rate'] = df['time_range']/df['visits']
    
    #логарифмируем среднее время на посещение
    df['visit_rate'] = np.log1p(df['visit_rate'])
    
    return df

df = feature_engineering(df)



def identity_tokenizer(text):
    return text

def tfidf(df):
    '''должна быть колонка domain_list'''
    
    def convert_to_df(data, df):    
        cols = list(map(lambda x: 'tfidf_'+str(x),np.arange(data.shape[1]))) 
        data = data.todense()
        data = np.squeeze(np.asarray(data))
        data = pd.DataFrame(data, columns = cols, index = df.index, dtype = np.float16)
        
        return pd.concat([data,df],axis=1), cols
    
    #tfidf

    tfidf_model = pickle.load(open('content_bigdata10_proj1/models/tfidf.pkl', 'rb'))
    
    data = tfidf_model.transform(df['domain_list'])
    # tsvd = TruncatedSVD(n_components=200)
    # svd_data = tsvd.fit_transform(sparse_tfidf_domain_list)
    
    data, cols = convert_to_df(data, df)
    
    
    return data, cols

df, cols = tfidf(df)


def lda(df, cols):
    '''должна быть колонка domain_list'''
    
    def convert_to_df(data, df):    
        cols = list(map(lambda x: 'lda_'+str(x),np.arange(data.shape[1])))
        data = pd.DataFrame(data, columns = cols, index = df.index, dtype = np.float16)
        
        return pd.concat([data,df],axis=1), cols
    

    lda_model = pickle.load(open('content_bigdata10_proj1/models/lda.pkl', 'rb'))
    
    data = lda_model.transform(df[cols])
    # tsvd = TruncatedSVD(n_components=200)
    # svd_data = tsvd.fit_transform(sparse_tfidf_domain_list)
    
    data, cols = convert_to_df(data, df)
    
    
    return data, cols

df, cols_lda = lda(df, cols)


model_gender = lgb.Booster(model_file='content_bigdata10_proj1/models/vb_lgb_model_gender.txt')
model_age = lgb.Booster(model_file='content_bigdata10_proj1/models/vb_lgb_model_age.txt')

df['predict']  = model_gender.predict(df[model_gender.feature_name()])

mask = (df['predict']<0.40) | (df['predict']>0.63)
#df = df[mask]

df['predict'] = df['predict']>0.5174055011345399
df['gender'] = np.vectorize(dict_gendercategory_to_gender.__getitem__)(df['predict'])
df.loc[~mask,'gender'] = '-'

df['predict'] = np.argmax(model_age.predict(df[model_gender.feature_name()]),axis=1)
df['age'] = np.vectorize(dict_agecategory_to_age.__getitem__)(df['predict'])
df.loc[~mask,'age'] = '-'

df = df[['uid', 'gender', 'age']]
df.sort_values(by='uid',axis = 0, ascending = True, inplace = True)
sys.stdout.write(df.to_json(orient='records'))


# vladislav.boyadzhi@master:~$ cp /data/home/vladislav.boyadzhi/content_bigdata10_proj1/notebooks/vb_project01_gender-age.py ~/project01_gender-age.py 
# vladislav.boyadzhi@master:~$ tail -n1000 /data/share/project01/gender_age_dataset.txt | /data/home/vladislav.boyadzhi/project01_gender-age.py > output.json



#cp /data/home/vladislav.boyadzhi/content_bigdata10_proj1/notebooks/vb_project01_gender-age.py ~/project01_gender-age.py 
#chmod +x vb_project01_gender-age.py 

#!tail -n1000 /data/share/project01/gender_age_dataset.txt | /data/home/vladislav.boyadzhi/content_bigdata10_proj1/notebooks/vb_project01_gender-age.py > output.json
