import praw
import urllib3
import os
from bs4 import BeautifulSoup
import certifi
import requests
import datetime
import pytz

from databasewrapper import DatabaseWrapper


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
        # '''elif 'imgur.com/' in url:
        #     print('imgur album handling...')
        #     urls = parse_album(url)
        #     if urls:
        #         url = urls[0]
        #         if url.endswith('mp4'):
        #             output['sitetag'] = 'imgurgifv'
        #             output['url'] = url.replace('mp4', 'jpg')
        #             output['mp4'] = url
        #             #output['urls'] = urls
        #         elif url.endswith(('jpg', 'JPG', 'png', 'PNG')):
        #             output['sitetag'] = 0
        #             output['url'] = url
        #         else:
        #             pass
        #     else:
        #         output = {}'''
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
    for submission in reddit.subreddit(subreddit).hot(limit=25):
        if not submission.url.endswith(('.jpg', '.JPG', '.png')):
            output = url_parser(submission.url)
            if output:
                yield (output, submission.id, submission.score, submission.title, submission.created)
            else:
                pass
        else:
            if 'gifly' in submission.url:
                pass
            else:
                output = {'url':submission.url, 'sitetag':0}
                yield (output,submission.id, submission.score, submission.title, submission.created)

def getSubmissionslocal(subreddit, subredditid):
    result = []
    db_items = []
    for item in pic_getter(subreddit):
        db_items.append(item)
    for item in db_items:
        output = item[0]
        #print(output.get('url'), output.get('sitetag'), output.get('mp4'), item[1], item[2])
        url = output.get('url')
        sitetag = output.get('sitetag')
        mp4 = output.get('mp4')
        submissionid = item[1]
        score = item[2]
        title = item[3]
        time = item[4]
        created = datetime.datetime.fromtimestamp(time)
        result.append((submissionid, title, score, url, mp4, sitetag, created, subreddit, subredditid))
    return result

def main():
    db = DatabaseWrapper('scrap_submission')
    db.get_new_connection()
    subredditslist = db.conn.execute('SELECT * FROM scrap_subredditslist')
    subredditslist = [(row[1], row[0], row[2]) for row in subredditslist]
    for sub in subredditslist:
        outputs = getSubmissionslocal(sub[0], sub[1])
        nsfw = sub[2]
        for output in outputs:
            try:
                output = (output[0], output[1], output[2], output[3], output[4], nsfw, output[5], output[6], output[7], output[8])
                print(output)
                db.conn.execute('INSERT INTO scrap_submission(id, title, score, url, mp4, nsfw, sitetag, created, subreddit, subredditid) VALUES (?,?,?,?,?,?,?,?,?,?)', output)
                db.conn.commit()
            except Exception as e:
                print(e)
    db.upload_database()
main()
    
