from django import forms
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Websites, Search

class SearchForm(forms.Form):
    terms_en = forms.CharField(label='Search terms', max_length=50, min_length=5)
    websites = forms.ModelMultipleChoiceField(
        queryset=Websites.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class RemoveForm(forms.Form):
    pk = forms.IntegerField(validators=[MinValueValidator(0)], widget=forms.HiddenInput())