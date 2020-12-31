from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class SearchForm(forms.Form):
    terms = forms.CharField(label='Search terms', max_length=100, min_length=6)

class RemoveForm(forms.Form):
    pk = forms.IntegerField(validators=[MinValueValidator(0)])