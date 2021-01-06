from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm, RemoveForm
from .models import Search, Websites
from account.models import User

# main page for Search objects where all searches for the current user are displayed
def index(request):
    current_user = request.user
    current_objects = Search.objects.filter(user=current_user.id)
    
    # POST request, receive either a remove form or a search form
    if request.method == 'POST':
        formR = RemoveForm(request.POST)
        formS = SearchForm(request.POST)

        # remove form is valid, so remove the given object from the database
        if formR.is_valid():
            try:
                s = Search.objects.get(pk=formR.cleaned_data['pk'])
                if current_user.id == s.user.pk:
                    s.delete()
            except:
                # User edited the HTML to submit the form with an invalid key
                pass

        # search form is valid, so add the given object to the database
        elif formS.is_valid():
            if (len(current_objects) < current_user.limit):
                s = Search(terms_en=formS.cleaned_data['terms_en'], user=current_user)
                s.save()
                for site in formS.cleaned_data['websites']:
                    s.websites.add(site)            
                s.save()
            else:
                # TODO: error, at limit
                pass
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
    count = Search.objects.filter(user=request.user.id).count()
    return render(request, 'notifications/new.html', {'form': form, 'count': count})