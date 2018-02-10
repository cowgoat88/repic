from bs4 import BeautifulSoup
import urllib3
import certifi
from pprint import pprint
import os
import sys
import django
import django.apps
import settings as myapp
from django.conf import settings
dir_path = os.path.dirname(os.getcwd())
sys.path.append(dir_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'repicScraper.settings')

django.setup()

from scrap.models import SubredditsList

url = 'https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits'
manager = urllib3.PoolManager(
      cert_reqs='CERT_REQUIRED',
      ca_certs=certifi.where()
  )
response = manager.request('GET', url)
html = response.data
soup = BeautifulSoup(html, 'html.parser')
wiki = soup.find('div', {'class':'wiki'})
children = wiki.findChildren()

(cat1, cat2, cat3) = ('','','')
catedict = {'h1':cat1,'h2':cat2,'h3':cat3}

for child in children:
    if child.name in catedict:
        catedict[child.name] = child.string
    elif child.name == 'a' and child.string.startswith('/r/'):
        if catdict['h2'] == 'Gifs' or catdict['h2'] == 'Images':
            sublist = SubredditsList(subreddit=child.string[3:], nsfw=1, cat1=catdict['h1'], cat2=catdict['h2'], cat3=catdict['h3'])
            sublist.save()