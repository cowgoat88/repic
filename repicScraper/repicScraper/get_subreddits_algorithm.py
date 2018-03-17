# -*- coding: utf-8 -*-
import praw
from databasewrapper import DatabaseWrapper

def subreddit_getter():
    subreddits_list = []
    reddit = praw.Reddit(client_id='XXD7dG6-YMzifw',client_secret='3AZn44eqfJHjjeGOLddcy19AJl4',password='wilder',user_agent='test by /u/repic-bot',username='repicbot')

    db = DatabaseWrapper('sqlite.db', 'scrap_subredditslist')
    db.get_new_connection()
    subreddits = db.get_all_subreddits()
    db.close()
    for submission in reddit.subreddit('all').hot(limit=10):
        if submission.subreddit.id not in [x[0] for x in subreddits_list] + subreddits:
            print('new = ', submission.subreddit.display_name)
            if submission.over_18 == True:
                subreddits_list.append((submission.subreddit.id, submission.subreddit.display_name, 1))
            else:
                subreddits_list.append((submission.subreddit.id, submission.subreddit.display_name, 0))
        else:
            print('duplicate = ', submission.subreddit.display_name)
    return subreddits_list

def subreddit_updater(new_to_add):
    print(new_to_add)
    sql = "INSERT INTO scrap_subredditslist VALUES (?,?,?,?,?,?)"

    db = DatabaseWrapper('sqlite.db', 'scrap_subredditslist')
    db.get_new_connection()
    max_id = db.get_max_id()
    for subreddit in new_to_add:
        max_id += 1
        cursor = db.conn.cursor()
        cursor.execute(sql, (max_id, subreddit[1], subreddit[2], 'all', '', ''))
        db.conn.commit()
    db.close()

new_subs_to_add = subreddit_getter()
subreddit_updater(new_subs_to_add)
