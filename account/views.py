from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponseRedirect

from .forms import RegistrationForm, GroupForm

def register(request):
    # POST request, creates a new user from the form and logs in
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('index')
        # else, render the page with the current form and errors again
    
    # GET request, creates a blank form for a user to create an account
    else:
        # redirects to the main page if a user is already logged in
        if request.user.is_authenticated:
            return redirect('index')
        else:
            form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def settings(request):
    if request.method == 'POST':
        group = GroupForm(request.POST)
        if group.is_valid() and request.user.is_authenticated:
            request.user.limit = group.cleaned_data.get('group')
            request.user.save()
            return redirect('index')

    else:
        group = GroupForm()

    return render(request, 'account/settings.html', {'group': group})