from django.contrib.auth.models import User
from django import forms
from . import models

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    
    # Also add password requirements

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match!')
        return cd['password2']
    
    def clean_email(self):
         data = self.cleaned_data['email']
         if User.objects.filter(email=data).exists():
              raise forms.ValidationError('Email already exist')
         return data
    

    
class UserEditForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email']
        
        def clean_email(self):
         data = self.cleaned_data['email']
         qs = User.objects.exclude(id=self.instance.id).filter(email=data)
         if qs.exists():
              raise forms.ValidationError('Email aleady exists.')
         return data

class ProfileEditForm(forms.ModelForm):
        class Meta:
            model = models.Profile
            fields = ['date_of_birth', 'photo']
    
