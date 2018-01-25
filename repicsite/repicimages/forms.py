from django import forms
import requests

'''
Need a programmable way to get this list
'''
db_json = requests.get('https://baj8ppw3tg.execute-api.us-east-1.amazonaws.com/dev/subredditslist/subredditsList/')
SUBREDDITS = [(item.get('subreddit'),item.get('subreddit')) for item in db_json.json()]


class SplashFilter(forms.Form):
	choice_field = forms.MultipleChoiceField(
        required=False,
        label='Choose what you want to see:',
        widget=forms.CheckboxSelectMultiple,
        choices=SUBREDDITS
    )

