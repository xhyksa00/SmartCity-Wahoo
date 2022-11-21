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

class RoleChangeForm(forms.Form):
    class Meta:
        fields = ['role']
        choices = [('Citizen','Citizen'),('Technician', 'Technician'), ('Officer', 'Officer')]

    role = forms.ChoiceField(choices=Meta.choices)

    def __init__(self, *args, **kwargs):
        super(RoleChangeForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['onchange'] =  'this.form.submit()'