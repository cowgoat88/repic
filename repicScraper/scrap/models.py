# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from decimal import Decimal
from django.forms import ModelForm

# Create your models here.
class Submission(models.Model):
    id = models.CharField(primary_key=True, null=False, max_length=15)
    title = models.CharField(max_length=40)
    score = models.IntegerField()
    url = models.CharField(max_length=200)
    mp4 = models.CharField(max_length=200, null=True)
    nsfw = models.IntegerField(null=True)
    sitetag = models.CharField(max_length=15)
    created = models.DateTimeField(null=False)
    
class SubredditsList(models.Model):
    id = models.AutoField(primary_key=True, null=False, max_length=5)
    subreddit = models.CharField(max_length=30)
    nsfw = models.IntegerField(null=True)
    
    
    