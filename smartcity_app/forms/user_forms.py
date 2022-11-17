from django import forms

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

class RegisterForm(forms.Form):
    email = forms.CharField()
    first_name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField()
    password_repeat = forms.CharField()

