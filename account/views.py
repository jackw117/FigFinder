from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect


def register(request):
    # POST request, creates a new user from the form and logs in
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('index')
        # else, render the page with the current form and errors again
    
    # GET request, creates a blank form for a user to create an account
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})    