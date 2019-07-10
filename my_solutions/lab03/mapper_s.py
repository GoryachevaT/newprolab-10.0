#!/opt/anaconda/envs/bd9/bin/python3

from urllib.parse import urlparse, unquote
import re
import sys

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
       return

for line in sys.stdin:
    tmp = line.strip().split('\t')
    if len(tmp) == 3:
        uid = tmp[0]
        url = url2domain(tmp[2])
        if uid != '-' and url != '' :
            print(uid,'\t', url.strip())

