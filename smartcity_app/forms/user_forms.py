from django import forms
from ..models import User

class LoginForm(forms.Form):
    email = forms.CharField(widget = forms.EmailInput())
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        fields = ['email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'


class RegisterForm(forms.Form):
    first_name = forms.CharField()
    surname = forms.CharField()
    email = forms.CharField(widget = forms.EmailInput())
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        fields = ['email','first_name', 'surname', 'password', 'confirm_password']


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'

class OfficerRoleForm(forms.Form):
    class Meta:
        fields = ['role']
        choices = [('Citizen','Citizen'),('Technician', 'Technician')]

    role = forms.ChoiceField(choices=Meta.choices)

    def __init__(self, *args, **kwargs):
        super(OfficerRoleForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['onchange'] =  'this.form.submit()'



class EditAccountForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'surname']
        model = User


    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget = forms.PasswordInput())
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        fields = ['old_password', 'password', 'confirm_password']


    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'
        