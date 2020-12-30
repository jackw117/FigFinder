from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm
from .models import Search    

def index(request):
    current_user = request.user
    data = Search.objects.filter(user_id=current_user.id)
    return render(request, 'notifications/index.html', {'data': data, 'user': current_user})

def new_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            s = Search(terms=form.cleaned_data['terms'], user_id=request.user.id)
            s.save()
            return HttpResponseRedirect('/notifications/')
    else:
        form = SearchForm()
    
    return render(request, 'notifications/new.html', {'form': form})