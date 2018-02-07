# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Submission(models.Model):
    class Meta:
        db_table = 'scrap_submission'
    id = models.CharField(primary_key=True, null=False, max_length=15)
    title = models.CharField(max_length=40)
    score = models.IntegerField()
    url = models.CharField(max_length=200)
    mp4 = models.CharField(max_length=200, null=True)
    nsfw = models.IntegerField(null=True)
    sitetag = models.CharField(max_length=15)
    created = models.DateTimeField(null=False)
    subreddit = models.CharField(max_length=20)
    subredditid = models.IntegerField(null=True)
    
class SubredditsList(models.Model):
    class Meta:
        db_table = 'scrap_subredditslist'
    id = models.AutoField(primary_key=True, null=False, max_length=5)
    subreddit = models.CharField(max_length=30)
    nsfw = models.IntegerField(null=True)
    cat1 = models.CharField(max_length=30, default=None, null=True)
    cat2 = models.CharField(max_length=30, default=None, null=True)
    cat3 = models.CharField(max_length=30, default=None, null=True)