from django import forms
from scrap.models import SubredditsList

SUBREDDITS = [(item.id,item.subreddit) for item in SubredditsList.objects.all()]

class SplashFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=forms.CheckboxSelectMultiple(attrs={'class':'form-checkbox'}),
        choices=SUBREDDITS,
    )

