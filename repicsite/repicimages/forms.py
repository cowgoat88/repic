from django import forms
from scrap.models import SubredditsList


SUBREDDITS = [(item.id,item.subreddit) for item in SubredditsList.objects.filter(nsfw=0)]
SUBREDDITS_NSFW_ONLY = [(item.id,item.subreddit) for item in SubredditsList.objects.filter(nsfw=1)]
SUBREDDITS_ALL = [(item.id,item.subreddit) for item in SubredditsList.objects.all()]
NSFW = [('allow','Include NSFW?'),('only','Only NSFW?')]

class SplashFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required = False,
        label = '',
        widget = forms.CheckboxSelectMultiple(attrs={'class':'form-checkbox'}),
        choices = SUBREDDITS,
    )

class FilterAll(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=SUBREDDITS_ALL,
    )

class NsfwOnlyFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=SUBREDDITS_NSFW_ONLY,
    )


class NsfwAllow(forms.Form):
    nsfw_field = forms.MultipleChoiceField(
        required = False,
        label = '',
        widget = forms.CheckboxSelectMultiple,
        choices = NSFW,
    )