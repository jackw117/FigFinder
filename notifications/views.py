from django.shortcuts import render
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime, timezone

from .forms import SearchForm, RemoveForm
from .models import Search, Websites, Details, Entry
from account.models import User

# main page for Search objects where all searches for the current user are displayed
def index(request):
    current_user = request.user
    current_objects = Search.objects.filter(user=current_user) if not current_user.is_anonymous else []
    
    # POST request, receive either a remove form or a search form
    if request.method == 'POST':
        formR = RemoveForm(request.POST)
        formS = SearchForm(request.POST)

        # remove form is valid, so remove the given object from the database
        if formR.is_valid():
            try:
                s = Search.objects.get(pk=formR.cleaned_data['pk'])
                if current_user == s.user:
                    s.delete()
            except:
                # User edited the HTML to submit the form with an invalid key
                pass

        # search form is valid, so add the given object to the database
        elif formS.is_valid():
            if (len(current_objects) < current_user.limit):
                terms = formS.cleaned_data['terms_en']
                s = Search.objects.create(terms_en=terms, user=current_user)
                for site in formS.cleaned_data['websites']:
                    details = getDetails(site, terms, None)
                    d = Details.objects.create(search=s, website=site)
                    for entry in details:
                        d.details.add(entry)
                        d.save()
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
    d = Details.objects.filter(search__pk=pk, search__user=request.user) if not request.user.is_anonymous else []
    if d:
        newDetails = []
        for item in d:
            diff = datetime.now(timezone.utc) - item.time
            if diff.total_seconds() >= 1 * 60:
                entries = getDetails(item.website, item.search.terms_en, item.details)
                item.details.clear()
                for e in entries:
                     item.details.add(e)
                item.time = datetime.now(tz=timezone.utc)
                item.save()
            newDetails.append(item)
        return render(request, 'notifications/details.html', {'details': newDetails})
    else:
        return render(request, 'notifications/details.html', {'details': []})

# TODO: fix adult confirm, fix breaking on space in item, check that updating new field works
def getDetails(site, item, details):
    className = ""
    if site.name != "Mandarake" and site.name != "Surugaya":
        return []        

    http = urllib3.PoolManager()
    right = site.url_right if site.url_right else ""
    sock = http.request('GET', site.url + item + right)
    soup = BeautifulSoup(sock.data, features='html.parser')
    divs = soup.find_all("div", class_=site.className)
    links = []
    for div in divs:
        links.append(div.find("a"))
    entries = []
    for link in links:
        url = link["href"]
        if not site.base_url in link["href"]:
            url = site.base_url + url
        e = Entry.objects.get_or_create(name=link.text, url=url)
        e[0].new = e[1]
        e[0].save()
        entries.append(e[0])
    sock.close()
    return entries