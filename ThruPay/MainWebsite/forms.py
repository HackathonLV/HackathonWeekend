from django import forms
from django.contrib.auth import authenticate
from django.forms import TextInput, PasswordInput, CheckboxInput


class LoginForm(forms.Form):
    username = forms.CharField(label='username', widget=TextInput())
    password = forms.CharField(label='password', widget=PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.cleaned_data['user'] = username
        self.cleaned_data['password'] = password
        return self.cleaned_data

