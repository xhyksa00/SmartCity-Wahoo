from django import forms
from ..models import Ticket, Image, TicketComments

PRIORITY_CHOICES = [
    ('Lowest', 'Lowest'),
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Highest', 'Highest'),
]

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'priority', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Title'
            }),
            'priority': forms.Select(choices=PRIORITY_CHOICES, attrs={
                'class':'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Description - up to 1000 characters',
                'rows': '11',
                'cols': '90',
                'maxlength': '1000'
            }),
        }

class ChangeStateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['state']

        state_choices = [
            ('Open', 'Open'),
            ('Waiting For Approval', 'Waiting'),
            ('In Progress', 'In Progress'),
            ('Closed: Denied', 'Closed: Denied'),
            ('Closed: Fixed', 'Closed: Fixed'),
            ('Closed: Duplicate', 'Closed: Duplicate'),
        ]
    state = forms.ChoiceField(choices=Meta.state_choices)

    def __init__(self, *args, **kwargs):
        super(ChangeStateForm, self).__init__(*args, **kwargs)


        # self.fields['state'].widget.choices = state_choices
        self.fields['state'].widget.attrs['onchange'] = 'this.form.submit()'

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['url']
        widgets = {
            'url': forms.ClearableFileInput(attrs={
                # 'class':'form-control',
                'multiple': True
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = TicketComments
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={
                'class':'form-control',
                'rows' : '3'
            }),
        }

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['priority']
        prio_choices = [
            ('Lowest','Lowest'),
            ('Low','Low'),
            ('Medium','Medium'),
            ('High','High'),
            ('Highest','Highest')
        ]

    priority = forms.ChoiceField(choices=Meta.prio_choices)

    def __init__(self, *args, **kwargs):
        super(PriorityForm, self).__init__(*args, **kwargs)

        self.fields['priority'].widget.attrs['onchange'] = 'this.form.submit()'

class TicketFilterForm(forms.Form):
    class Meta:
        fields = ['search', 'priority', 'state', 'order', 'order_by']

        priority_choices = [
            ('any', 'Any'),
            ('Lowest', 'Lowest'),
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Highest', 'Highest'),
        ]

        order_choices = [
            ('asc', 'Ascending'),
            ('dsc', 'Descending'),
        ]

        state_choices = [
            ('any', 'Any'),
            ('Open', 'Open'),
            ('Waiting', 'Waiting'),
            ('In Progress', 'In Progress'),
            ('Closed: Denied', 'Closed: Denied'),
            ('Closed: Fixed', 'Closed: Fixed'),
            ('Closed: Duplicate', 'Closed: Duplicate'),
        ]

        order_by_choices = [
            ('id', 'ID'),
            ('title', 'Title'),
            ('priority', 'Priority'),
            ('created_timestamp', 'Date'),
            ('state', 'Status'),
        ]

    search = forms.CharField()
    priority = forms.ChoiceField(choices=Meta.priority_choices)
    state = forms.ChoiceField(choices=Meta.state_choices)
    order = forms.ChoiceField(choices=Meta.order_choices)
    order_by = forms.ChoiceField(choices=Meta.order_by_choices)

    def __init__(self, *args, **kwargs):
        super(TicketFilterForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].required = False
        self.fields['search'].widget.attrs['class'] = 'form-control'
        self.fields['search'].widget.attrs['placeholder'] = 'Search Ticekt titles and descriptions'
        self.fields['priority'].widget.attrs['class'] = 'form-select'
        self.fields['state'].widget.attrs['class'] = 'form-select'
        self.fields['order'].widget.attrs['class'] = 'form-select'
        self.fields['order_by'].widget.attrs['class'] = 'form-select'