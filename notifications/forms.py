from django import forms

class SearchForm(forms.Form):
    text = forms.CharField(label='Search terms', max_length=100)