from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm, RemoveForm
from .models import Search, Websites   

def index(request):
    current_user = request.user
    current_objects = Search.objects.filter(user_id=current_user.id)
    
    if request.method == 'POST':
        form = RemoveForm(request.POST)
        if form.is_valid():
            try:
                s = Search.objects.get(pk=form.cleaned_data['pk'])
                if current_user.id == s.user_id:
                    s.delete()
            except:
                # User submit the form with an invalid key
                pass
        return HttpResponseRedirect('')
    else:
        data = []
        for i in range(len(current_objects)):
            tup = (current_objects[i], RemoveForm(initial={'pk': current_objects[i].pk}))
            data.append(tup)
        return render(request, 'notifications/index.html', {'data': data, 'user': current_user})

# TODO: redirect to home after adding a notification
def new_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            s = Search(terms_en=form.cleaned_data['terms_en'], terms_jp=form.cleaned_data['terms_jp'], user_id=request.user.id)
            s.save()
            for site in form.cleaned_data['websites']:
                s.websites.add(site)            
            s.save()
        return HttpResponseRedirect('')
    else:
        form = SearchForm()
        return render(request, 'notifications/new.html', {'form': form})