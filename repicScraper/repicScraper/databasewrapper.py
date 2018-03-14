# -*- coding: utf-8 -*-
import boto3
import sqlite3
import os
from tempfile import gettempdir

class DatabaseWrapper():
    def __init__(self, database, table):
        # create lazy handle for remote object
        self.s3obj = self.get_s3_object()
        # set name of local copy
        self.local_db = os.path.abspath(os.path.join(gettempdir(), self.s3obj.key))
        self.database = database
        self.table = table

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
        sql = 'SELECT MAX(id) FROM {}'.format(self.table)
        c = self.conn.cursor()
        c.execute(sql)
        max_id = c.fetchone()
        return max_id[0]

    def get_all_subreddits(self):
        sql = 'SELECT subredditid FROM scrap_subredditslist'
        c = self.conn.cursor()
        c.execute(sql)
        return [row[0] for row in c.fetchall()]
