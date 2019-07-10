#!/opt/anaconda/envs/bd9/bin/python3

import sys
from  urllib.parse import urlparse, unquote
import urllib
import re

def url2domain(url):
   try:
       a = urlparse(unquote(url.strip()))
       if (a.scheme in ['http','https']):
           b = re.search("(?:www\.)?(.*)",a.netloc).group(1)
           if b is not None:
               return str(b).strip()
           else:
               return ''
       else:
           return ''
   except:
       print("ca not parse ", url.strip(), unquote(url.strip()))
       return

for line in sys.stdin:
    line = line.strip()
    elements = line.split('\t')
    if len(elements) == 3:
        uid, ts, url_string = elements
        url = url2domain(url_string)
        if url == '': continue
        print( ','.join([uid, ts, url]))

