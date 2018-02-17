# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib3
import certifi
from databasewrapper import DatabaseWrapper

def main():
    baseurl = 'https://www.reddit.com/r/ListOfSubreddits/wiki/'
    uris = {
        'listofsubreddits': {
            'nsfw': 0,
            'cat': 'h2'
        },
        'nsfw': {
            'nsfw': 1,
            'cat': 'h1'
        }
    }
    manager = urllib3.PoolManager(
          cert_reqs='CERT_REQUIRED',
          ca_certs=certifi.where()
    )
    
    db = DatabaseWrapper()
    db.get_new_connection()
    max_id = db.get_max_id()
    subreddits = db.get_all_subreddits()
    
    sql = "INSERT INTO scrap_subredditslist VALUES (?,?,?,?,?,?)"
    
    for uri in uris:
        url = baseurl + uri
        nsfw = uris[uri]['nsfw']
        response = manager.request('GET', url)
        html = response.data
        soup = BeautifulSoup(html, 'html.parser')
        wiki = soup.find('div', {'class':'wiki'})
        children = wiki.findChildren()

        (cat1, cat2, cat3) = ('','','')
        catdict = {'h1':cat1,'h2':cat2,'h3':cat3}
        
        for child in children:
            if child.name in catdict:
                catdict[child.name] = child.string
            elif child.name == 'a' and child.string.startswith('/r/'):
                if catdict[uris[uri]['cat']] == 'Gifs' or catdict[uris[uri]['cat']] == 'Images':
                    if child.string[3:] not in subreddits:
                        max_id += 1
                        print(child.string, catdict['h1'], catdict['h2'], catdict['h3'])
                        cursor = db.conn.cursor()
                        cursor.execute(sql, (max_id, child.string[3:], nsfw, catdict['h1'], catdict['h2'], catdict['h3']))
                        db.conn.commit()
        db.close()
                
main()