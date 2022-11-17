from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label = 'Your name', max_length = 50)
    password = forms.CharField(label = 'Password', max_length = 50, widget=forms.PasswordInput)
    class Meta:
        fields = ['name', 'password']