from django.contrib import admin

# Register your models here.
from .models import Submission, SubredditsList

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'score', 'url', 'mp4', 'nsfw', 'sitetag', 'created', 'subreddit', 'subredditid')

@admin.register(SubredditsList)
class SubredditsAdmin(admin.ModelAdmin):
	list_display = ('id', 'subreddit', 'nsfw')
	