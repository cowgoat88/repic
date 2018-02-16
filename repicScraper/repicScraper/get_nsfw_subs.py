# -*- coding: utf-8 -*-
import boto3
import sqlite3
import os
from tempfile import gettempdir
from bs4 import BeautifulSoup
import urllib3
import certifi


def abspath_join(*args):
    return os.path.abspath(os.path.join(*args))
    
class DatabaseWrapper():

    def __init__(self):
        # create lazy handle for remote object
        self.s3obj = self.get_s3_object()
        # set name of local copy
        self.local_db = abspath_join(gettempdir(), self.s3obj.key)

    def get_s3_resource(self):
        # get s3 client
        return boto3.resource('s3')

    def get_s3_object(self):
        # get s3 object handle
        bucket_name = 'repic-db'
        key = 'sqlite.db'
        return self.get_s3_resource().Object(bucket_name, key)

    def get_new_connection(self):
        # download if necessary
        self.download_database()
        # point the default sqlite client/db wrapper to our local copy
        self.conn = sqlite3.connect(self.local_db)

    def download_database(self):
        # download database to temp file if necessary
        if not os.path.isfile(self.local_db):
            self.s3obj.download_file(self.local_db)

    def close(self):
        self.upload_database()
        self.conn.close()

    def upload_database(self):
        # upload the local copy on every close
        if os.path.isfile(self.local_db):
            self.s3obj.upload_file(self.local_db)
            
    def get_max_id(self):
        sql = 'SELECT MAX(id) FROM scrap_subredditslist'
        c = self.conn.cursor()
        c.execute(sql)
        max_id = c.fetchone()
        return max_id[0]
        
    def select_all(self):
        sql = 'SELECT * FROM scrap_subredditslist'
        c = self.conn.cursor()
        c.execute(sql)
        for row in c.fetchall():
            print(row)
            
def main():
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

    (cat1, cat2, cat3) = ('','','')
    catdict = {'h1':cat1,'h2':cat2,'h3':cat3}

    db = DatabaseWrapper()
    db.get_new_connection()
    max_id = db.get_max_id()
    
    sql = "INSERT INTO scrap_subredditslist VALUES (?,?,?,?,?,?)"
    for child in children:
        if child.name in catdict:
            catdict[child.name] = child.string
        elif child.name == 'a' and child.string.startswith('/r/'):
            if catdict['h1'] == 'Gifs' or catdict['h1'] == 'Images':
                max_id += 1
                print(child.string, catdict['h1'], catdict['h2'], catdict['h3'])
                cursor = db.conn.cursor()
                cursor.execute(sql, (max_id, child.string[3:], 1, catdict['h1'], catdict['h2'], catdict['h3']))
                db.conn.commit()
                
    db.close()
                
main()
