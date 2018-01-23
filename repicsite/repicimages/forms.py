from django import forms

class SplashFilter(forms.Form):
	firstName = forms.CharField(max_length=30, required=False)
	lastName = forms.CharField(max_length=30, required=False)