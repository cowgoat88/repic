from django import forms
import requests
from scrap.models import SubredditsList

SUBREDDITS = [(item.subreddit,item.subreddit) for item in SubredditsList.objects.all()]

class SplashFilter(forms.Form):
	choice_field = forms.MultipleChoiceField(
        required=False,
        label='Choose what you want to see:',
        widget=forms.CheckboxSelectMultiple,
        choices=SUBREDDITS
    )

