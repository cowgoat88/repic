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

url = 'https://www.reddit.com/r/ListOfSubreddits/wiki/nsfw'
manager = urllib3.PoolManager(
      cert_reqs='CERT_REQUIRED',
      ca_certs=certifi.where()
  )
response = manager.request('GET', url)
html = response.data
soup = BeautifulSoup(html, 'html.parser')
wiki = soup.find('div', {'class':'wiki'})
children = wiki.findChildren()
cat1 = ''
cat2 = ''
cat3 = ''
cat4 = ''
cat5 = ''
for child in children:
    if child.name == 'h1':
        cat1 = child.string
    if child.name == 'h2':
        cat2 = child.string
    if child.name == 'h3':
        cat3 = child.string
    if child.name == 'h4':
        cat4 = child.string
    if child.name == 'h5':
        cat5 = child.string
    if child.name == 'a':
        if child.string.startswith('/r/'):
            if cat1 in ['General', 'Age', 'Animated', 'BDSM', 'Blowjobs']:
                sublist = SubredditsList()
                sublist.subreddit = child.string[3:]
                sublist.nsfw = 1
                sublist.cat1 = cat1
                sublist.cat2 = cat2
                sublist.cat3 = cat3
                sublist.save()
            if cat1 == 'Amateur':
                if cat3 == 'Ethnicity':
                    sublist = SubredditsList()
                    sublist.subreddit = child.string[3:]
                    sublist.nsfw = 1
                    sublist.cat1 = cat1
                    sublist.cat2 = cat2
                    sublist.cat3 = cat3
                    sublist.save()
            if cat2 == 'Petite':
                sublist = SubredditsList()
                sublist.subreddit = child.string[3:]
                sublist.nsfw = 1
                sublist.cat1 = cat1
                sublist.cat2 = cat2
                sublist.cat3 = cat3
                sublist.save()