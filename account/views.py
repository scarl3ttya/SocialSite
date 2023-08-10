from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from . import forms, models

def home(request):
    return HttpResponse('<h1>Account Home</h1>')

def register(request):
    if request.method == 'post':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})

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
def edit(request):
    if request.method == 'post':
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'profile_form':profile_form, 'user_form':user_form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})