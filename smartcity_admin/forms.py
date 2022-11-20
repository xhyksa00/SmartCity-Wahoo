from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        fields = ['username' ,'password']
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'