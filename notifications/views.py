from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm
from .models import Search

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            s = Search(terms=form.cleaned_data['text'])
            s.save()
            return HttpResponseRedirect('/notifications/')
    else:
        form = SearchForm()
    
    return render(request, 'notifications/index.html', {'form': form})
