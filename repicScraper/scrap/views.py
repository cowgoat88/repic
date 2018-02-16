from .models import Submission, SubredditsList
from rest_framework import viewsets
from django.http import JsonResponse
from .serializers import SubmissionSerializer, SubredditsListSerializer
import praw
import urllib3
from bs4 import BeautifulSoup
import certifi
import requests
import datetime
from django.utils import timezone
import pytz
from zappa.async import task

def parse_album(url):
    manager = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    response = manager.request('GET', url)
    html = response.data
    soup = BeautifulSoup(html, 'html.parser')
    snippet = soup.findAll('div', {'class':'post-image'})
    links = []
    for div in snippet:
        for d in div.findAll():
            if d.name == 'img':
                post = d['src']
                links.append('https:' + post)
            if d.name == 'source':
                post = d['src']
                links.append('https:' + post)
    return links

def flickr_parser(url):
    if url.endswith('dateposted-public/'):
        url_ = url.split('/')
        u = '/'.join(url_[:-3])
        url_open = u + '/sizes/l'
    elif url.endswith('sizes/l'):
        url_open = url
    else:
        url_open = url + '/sizes/l'
    manager = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    response = manager.request('GET', url)
    html = response.data

    soup = BeautifulSoup(html, 'html.parser')

    f = [x['src'] for x in soup.findAll('img') if 'c1.staticflickr' in x['src']]
    if f:
        return f[0]
    else:
        return url

def url_parser(url):
    output = {}
    try:
        if 'gfycat' in url:
            output['sitetag'] = 'gfycat'
            s = url.split('/')
            s.insert(3, 'ifr')
            output['url'] = '/'.join(s)
        elif url.endswith('gifv'):
            output['sitetag'] = 'imgurgifv'
            output['url'] = url.replace('gifv', 'jpg')
            output['mp4'] = url.replace('gifv', 'mp4')

        elif 'flickr' in url:
            output['url'] = flickr_parser(url)
            output['sitetag'] = 'flickr'
        else:
            print('OUTLIER:', url)
        return output
    except Exception as e:
        print(e)
        return {}

def pic_getter(subreddit):
    reddit = praw.Reddit(client_id='XXD7dG6-YMzifw',client_secret='3AZn44eqfJHjjeGOLddcy19AJl4',password='wilder',user_agent='test by /u/repic-bot',username='repicbot')
    for submission in reddit.subreddit(subreddit[0]).hot(limit=25):
        if not submission.url.endswith(('.jpg', '.JPG', '.png')):
            output = url_parser(submission.url)
            if output:
                yield (output, submission.id, submission.score, submission.title, subreddit[1], submission.created, subreddit[0])
            else:
                pass
        else:
            if 'gifly' in submission.url:
                pass
            else:
                output = {'url':submission.url, 'sitetag':0}
                yield (output,submission.id, submission.score, submission.title, subreddit[1], submission.created, subreddit[0])

@task
def getSubmissions(subredditid):
    """
    asynchonous praw scraper.
    """
    subreddits = SubredditsList.objects.filter(pk=subredditid)
    sub = [(sub.subreddit, sub.nsfw) for sub in subreddits][0]
    print(sub)
    db_items = []
    for item in pic_getter(sub):
        db_items.append(item)
    submission = Submission()
    try:
        for item in db_items:
            output = item[0]
            #print(output.get('url'), output.get('sitetag'), output.get('mp4'), item[1], item[2])
            submission.url = output.get('url')
            submission.sitetag = output.get('sitetag')
            submission.mp4 = output.get('mp4')
            submission.id = item[1]
            submission.score = item[2]
            submission.title = item[3]
            submission.nsfw = item[4]
            time = item[5]
            submission.created = datetime.datetime.fromtimestamp(time, tz=pytz.UTC)
            submission.subreddit = item[6]
            subredditobj = SubredditsList.objects.get(subreddit=item[6])
            submission.subredditid = subredditobj.id
            print(submission)
            submission.save()
    except:
        pass

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows view of praw output
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    
class SubredditsListViewSet(viewsets.ModelViewSet):
    """
    API endpoint to get subreddits list
    """
    queryset = SubredditsList.objects.all()
    serializer_class = SubredditsListSerializer
    
def asyncScrap(request):
    subreddits = SubredditsList.objects.all()
    for subreddit in subreddits:
        subid = subreddit.id
        getSubmissions(subid)
    return JsonResponse({'status':'Success'}, status=200)
