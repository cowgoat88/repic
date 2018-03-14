# -*- coding: utf-8 -*-
import praw
from databasewrapper import DatabaseWrapper

def subreddit_getter():
    subreddits_list = []
    reddit = praw.Reddit(client_id='XXD7dG6-YMzifw',client_secret='3AZn44eqfJHjjeGOLddcy19AJl4',password='wilder',user_agent='test by /u/repic-bot',username='repicbot')
    for submission in reddit.subreddit('all').hot(limit=25):
        if submission.over_18 == True:
            subreddits_list.append((submission.subreddit.id, submission.subreddit.display_name, 1))
        else:
            subreddits_list.append((submission.subreddit.id, submission.subreddit.display_name, 0))

    db = DatabaseWrapper('sqlite.db', 'scrap_subredditslist')
    db.get_new_connection()
    max_id = db.get_max_id()
    subreddits = db.get_all_subreddits()
    print(subreddits_list)
    new_subreddits = [sub for sub in subreddits_list if sub[0] not in subreddits]
    print(new_subreddits)
'''
    sql = "INSERT INTO scrap_subredditslist VALUES (?,?,?,?,?,?)"

    for subreddit in new_subreddits:
        max_id += 1
        cursor = db.conn.cursor()
        cursor.execute(sql, (max_id, subreddit[0], subreddit[1], 'all', '', ''))
        db.conn.commit()
    db.close()
'''
subreddit_getter()
