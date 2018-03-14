from django import forms
from scrap.models import SubredditsList
from django.forms import widgets


curated_list = ['gifs', 'Natureisfuckinglit', 'funny', 'reactiongifs', 'pics']
pics_list = ['pics', 'gifs']
gifs_list = ['gifs', 'WastedGifs', 'reactiongifs']
funny_list = ['gifs', 'funny']
wild_list = ['gifs']

SUBREDDITS = [(item.id,item.subreddit) for item in SubredditsList.objects.filter(nsfw=0)]
SUBREDDITS_NSFW_ONLY = [(item.id,item.subreddit) for item in SubredditsList.objects.filter(nsfw=1)]
SUBREDDITS_ALL = [(item.id,item.subreddit) for item in SubredditsList.objects.all()]
SPLASH = [(item.id,item.subreddit) for item in SubredditsList.objects.all() if item.subreddit in curated_list]
PICS = [(item.id,item.subreddit) for item in SubredditsList.objects.all() if item.subreddit in pics_list]
GIFS = [(item.id,item.subreddit) for item in SubredditsList.objects.all() if item.subreddit in gifs_list]
FUNNY = [(item.id,item.subreddit) for item in SubredditsList.objects.all() if item.subreddit in funny_list]
WILD = [(item.id,item.subreddit) for item in SubredditsList.objects.all() if item.subreddit in wild_list]
NSFW = [('allow', 'Include NSFW?'),('only', 'Only NSFW?')]

#KICKASS META PROGRAMMING add the following class to widgets
widgets.__all__ = list(widgets.__all__).append('CustomCheckboxSelectMultiple')

class CustomCheckboxSelectMultiple(widgets.ChoiceWidget):
    allow_multiple_selected = True
    input_type = 'checkbox'
    template_name = 'widgets/checkbox_select_custom.html'
    option_template_name = 'widgets/checkbox_option.html'

    def use_required_attribute(self, initial):
        # Don't use the 'required' attribute because browser validation would
        # require all checkboxes to be checked instead of at least one.
        return False

    def value_omitted_from_data(self, data, files, name):
        # HTML checkboxes don't appear in POST data if not checked, so it's
        # never known if the value is actually omitted.
        return False

    def id_for_label(self, id_, index=None):
        """"
        Don't include for="field_0" in <label> because clicking such a label
        would toggle the first checkbox.
        """
        if index is None:
            return ''
        return super().id_for_label(id_, index)

class SplashFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required = False,
        label = '',
        widget = CustomCheckboxSelectMultiple(attrs={'class':'form-checkbox'}),
        choices = SPLASH,
    )

class FilterAll(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=SUBREDDITS_ALL,
    )
class FilterAllSafe(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=SUBREDDITS,
    )

class NsfwOnlyFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=SUBREDDITS_NSFW_ONLY,
    )

class picsFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=PICS,
    )

class gifsFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=GIFS,
    )

class funnyFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=FUNNY,
    )

class wildFilter(forms.Form):
    choice_field = forms.MultipleChoiceField(
        required=False,
        label='',
        widget=CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices=WILD,
    )

class NsfwAllow(forms.Form):
    nsfw_field = forms.MultipleChoiceField(
        required = False,
        label = '',
        widget = CustomCheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        choices = NSFW,
    )
