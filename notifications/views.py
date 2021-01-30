from django.shortcuts import render
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
import urllib3

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
                details = []
                terms = formS.cleaned_data['terms_en']
                for site in formS.cleaned_data['websites']:
                    if site.name == "Mandarake":
                        srcs = getDetails(site, terms, "pic")
                        for src in srcs:
                            details.append(src)
                    elif site.name == "Surugaya":
                        srcs = getDetails(site, terms, "item_detail")
                        for src in srcs:
                            details.append(src)

                s = Search(terms_en=terms, user=current_user, details=details)
                s.save()
                for site in formS.cleaned_data['websites']:
                    s.websites.add(site)
                s.save()

                tup = (s, RemoveForm(initial={'pk': s.pk}))
                return render(request, 'notifications/new.html', {'item': tup})
            else:
                # TODO: error, at limit
                return render(request, 'notifications/new.html')
        else:
            return render(request, 'notifications/new.html')
        return HttpResponseRedirect('')

    # GET request, display all searches for a current user on the page
    else:
        data = []
        new_form = SearchForm()
        for i in range(len(current_objects)):
            tup = (current_objects[i], RemoveForm(initial={'pk': current_objects[i].pk}))
            data.append(tup)
        return render(request, 'notifications/index.html', {'data': data, 'user': current_user, 'form': new_form})

def details(request, pk):
    try:
        s = Search.objects.get(pk=pk)
        if s.user == request.user:
            return render(request, 'notifications/details.html', {'search': s})
        # else:
        #     return HttpResponseRedirect('')
    except:
        # invalid pk
        pass
    return render(request, 'notifications/details.html', {'search': []})

# TODO: fix adult confirm

def getDetails(site, item, className):
    http = urllib3.PoolManager()
    right = site.url_right if site.url_right else ""
    sock = http.request('GET', site.url + item + right)
    soup = BeautifulSoup(sock.data)
    divs = soup.find_all("div", class_=className)
    links = []
    for div in divs:
        links.extend(div.find_all("a"))
    hrefs = []
    for link in links:
        if site.base_url in link["href"]:
            hrefs.append(link["href"])
        else:
            hrefs.append(site.base_url + link["href"])
    sock.close()
    return hrefs
# TODO: new model for details, add parser to soup