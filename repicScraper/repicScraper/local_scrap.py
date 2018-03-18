import praw
import urllib3
import os
from bs4 import BeautifulSoup
import certifi
import requests
import datetime
import pytz
from databasewrapper import DatabaseWrapper
import re


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
        elif url.endswith('gif'):
            output = {'url':url, 'sitetag':'gifv'}
        elif 'imgur.com/' in url:
            m = re.search('(?<=imgur.com/).{7}', url)
            check_this_url = 'https://i.imgur.com/{m.group(0)}.jpg'
            if requests.get(check_this_url).ok == True:
                output = {'url':check_this_url, 'sitetag':0}
                print(check_this_url)
            else:
                check_this_url = 'https://i.imgur.com/{m.group(0)}.mp4'
                if requests.get(check_this_url).ok == True:
                    output = {'url':check_this_url, 'sitetag':'imgurgifv'}
                    print(check_this_url)

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
            #print('OUTLIER:', url)
            pass
        return output
    except Exception as e:
        print(e)
        return {}

def pic_getter(subreddit):
    reddit = praw.Reddit(client_id='XXD7dG6-YMzifw',client_secret='3AZn44eqfJHjjeGOLddcy19AJl4',password='wilder',user_agent='test by /u/repic-bot',username='repicbot')
    image_metric = 15
    submissions_db = DatabaseWrapper('sqlite.db', 'scrap_submission')
    submissions_db.get_new_connection()
    submissions_ids = [row[0] for row in submissions_db.conn.execute('SELECT id FROM scrap_submission')]
    submissions_db.close()
    print(subreddit, '\t=============')

    for submission in reddit.subreddit(subreddit).hot(limit=25):
        if submission.id in submissions_ids:
            pass
        else:
            if not submission.url.endswith(('.jpg', '.JPG', '.png')):
                output = url_parser(submission.url)
                if output:
                    image_metric += 1
                    yield (output, submission.id, submission.score, submission.title, submission.created)
                else:
                    image_metric -= 1
                    print(image_metric)
                    pass
            else:
                if 'gifly' in submission.url:
                    pass
                else:
                    image_metric += 1
                    output = {'url':submission.url, 'sitetag':0}
                    yield (output,submission.id, submission.score, submission.title, submission.created)
            if image_metric < 1:
                print(subreddit, 'low image count')
                sub_db = DatabaseWrapper('sqlite.db', 'scrap_subredditslist')
                sub_db.get_new_connection()
                cursor = sub_db.conn.cursor()
                cursor.execute("""  UPDATE scrap_subredditslist
                                    SET cat3 = 'hide'
                                    WHERE subreddit = ?""", (subreddit,))
                sub_db.conn.commit()
                sub_db.close()
                return False



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
    db = DatabaseWrapper('sqlite.db', 'scrap_submission')
    db.get_new_connection()
    subredditslist = db.conn.execute('SELECT * FROM scrap_subredditslist')
    subredditslist = [(row[1], row[0], row[2]) for row in subredditslist]
    db.close()

    for sub in subredditslist:
        outputs = getSubmissionslocal(sub[0], sub[1])
        nsfw = sub[2]
        for output in outputs:
            try:
                print(output)
                output = (output[0], output[1], output[2], output[3], output[4], nsfw, output[5], output[6], output[7], output[8])
                #print(output)
                db.get_new_connection()
                db.conn.execute('INSERT INTO scrap_submission(id, title, score, url, mp4, nsfw, sitetag, created, subreddit, subredditid) VALUES (?,?,?,?,?,?,?,?,?,?)', output)
                db.conn.commit()
                db.close()
            except Exception as e:
                print(e)
    db.get_new_connection()
    db.upload_database()
    db.close()
main()
