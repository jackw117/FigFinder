from django import forms

class SearchForm(forms.Form):
    terms = forms.CharField(label='Search terms', max_length=100)