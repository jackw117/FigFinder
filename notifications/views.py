from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm, RemoveForm
from .models import Search, Websites   

# main page for Search objects where all searches for the current user are displayed
def index(request):
    current_user = request.user
    current_objects = Search.objects.filter(user_id=current_user.id)
    
    # POST request, receive either a remove form or a search form
    if request.method == 'POST':
        formR = RemoveForm(request.POST)
        formS = SearchForm(request.POST)

        # remove form is valid, so remove the given object from the database
        if formR.is_valid():
            try:
                s = Search.objects.get(pk=formR.cleaned_data['pk'])
                if current_user.id == s.user_id:
                    s.delete()
            except:
                # User submit the form with an invalid key
                pass

        # search form is valid, so add the given object to the database
        elif formS.is_valid():
            s = Search(terms_en=formS.cleaned_data['terms_en'], terms_jp=formS.cleaned_data['terms_jp'], user_id=request.user.id)
            s.save()
            for site in formS.cleaned_data['websites']:
                s.websites.add(site)            
            s.save()
        return HttpResponseRedirect('')

    # GET request, display all searches for a current user on the page
    else:
        data = []
        for i in range(len(current_objects)):
            tup = (current_objects[i], RemoveForm(initial={'pk': current_objects[i].pk}))
            data.append(tup)
        return render(request, 'notifications/index.html', {'data': data, 'user': current_user})

# page for adding a new Search object
def new_search(request):
    form = SearchForm()
    return render(request, 'notifications/new.html', {'form': form})