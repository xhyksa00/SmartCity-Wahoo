from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['old_password', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'


class RoleChangeForm(forms.Form):

    class Meta:
        fields = ['role']
        choices = [('Citizen', 'Citizen'), ('Technician',
                                            'Technician'), ('Officer', 'Officer')]

    role = forms.ChoiceField(choices=Meta.choices)

    def __init__(self, *args, **kwargs):
        super(RoleChangeForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['onchange'] = 'this.form.submit()'


class UserFilterForm(forms.Form):

    class Meta:
        fields = ['name','surname','role', 'id', 'order_by', 'order']
        role_choices = [('any','Any'),('Citizen', 'Citizen'), ('Technician', 'Technician'), ('Officer', 'Officer')]
        order_choices = [('id', 'ID'),('name', 'Name'),('surname', 'Surname'),('role', 'Role') ]
        ascend_choices = [('ascending', 'Ascending'),('descending', 'Descending')]

    name = forms.CharField()
    surname = forms.CharField()
    role = forms.ChoiceField(choices=Meta.role_choices)
    id = forms.CharField(widget= forms.NumberInput())
    order_by = forms.ChoiceField(choices=Meta.order_choices)
    order = forms.ChoiceField(choices=Meta.ascend_choices)

    def __init__(self, *args, **kwargs):
        super(UserFilterForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['class'] = 'form-control'
            self.fields[fieldName].required = False

