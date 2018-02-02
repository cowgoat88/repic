from django import forms
from scrap.models import SubredditsList


SUBREDDITS = [(item.id,item.subreddit) for item in SubredditsList.objects.filter(nsfw=0)]
SUBREDDITS_NSFWONLY = [(item.id,item.subreddit) for item in SubredditsList.objects.filter(nsfw=1)]
SUBREDDITS_ALL = [(item.id,item.subreddit) for item in SubredditsList.objects.all()]
NSFW = [(True,'Include NSFW?')]

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


class NsfwFilter(forms.Form):
    nsfw_field = forms.MultipleChoiceField(
        required = False,
        label = '',
        widget = forms.CheckboxSelectMultiple(attrs={'class': 'nfsw-checkbox'}),
        choices = NSFW,
    )