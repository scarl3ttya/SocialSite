from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from . import forms

def home(request):
    return HttpResponse('<h1>Account Home</h1>')

def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user) # set user session info
                    return HttpResponse('Login successful')
                else:
                    return HttpResponse('Disabled Acct')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = forms.LoginForm()
        return render(request, 'account/login.html', {'form':form})
    
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})