from django.contrib import admin

# Register your models here.
from .models import Submission, SubredditsList

@admin.register(Submission)
class ExplorationsAdmin(admin.ModelAdmin):
    pass

@admin.register(SubredditsList)
class SubredditsAdmin(admin.ModelAdmin):
    pass