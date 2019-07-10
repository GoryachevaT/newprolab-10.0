#!/opt/anaconda/envs/bd9/bin/python
import sys
import re

def parse_site(url): #recommended function from task
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

allowed_urls = [u'cars.ru', u'avto-russia.ru', u'bmwclub.ru', u'postnauka.ru', u'plantarium.ru', u'lensart.ru', u'pass.rzd.ru', u'rzd.ru', u'vokrug.tv',
u'apteka.ru', u'doctor.ufacity.info', u'womanhit.ru']

for line in sys.stdin:
    tokens = line.strip().split("\t")
    if len(tokens) != 3 or not tokens[0] or not tokens[2] or tokens[0] == '-':
        continue
    site = parse_site2(tokens[2])
    if site not in allowed_urls:
        continue
    print ("%s\t%s" % (tokens[0], site))