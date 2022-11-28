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

class PriorityForm(forms.Form):
    class Meta:
        fields = ['priority']
        choices = [('Lowest','Lowest'),('Low','Low'),('Medium','Medium'),('High','High'),('Highest','Highest')]

    priority = forms.ChoiceField(choices=Meta.choices)

    def __init__(self, *args, **kwargs):
        super(PriorityForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].widget.attrs['onchange'] =  'this.form.submit()'

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
            ('title', 'Title'),
            ('priority', 'Priority'),
            # ('date', 'Date'),
            ('state', 'State'),
        ]

        # fields = ['priority', 'state', 'order', 'order_by']
        # labels = {
        #     'search': 'Search Title and Description',
        #     'priority': 'Priority',
        #     'state': 'Status',
        #     'order': 'Order',
        #     'order_by': 'Order by',
        # }
        # widgets = {
        #     'search': forms.CharField(),
        #     'priority': forms.ChoiceField(choices=priority_choices),
        #     'state': forms.ChoiceField(choices=state_choices),
        #     'order': forms.ChoiceField(choices=order_choices),
        #     'order_by': forms.ChoiceField(choices=order_by_choices),
        # }
    search = forms.CharField()
    priority = forms.ChoiceField(choices=Meta.priority_choices)
    state = forms.ChoiceField(choices=Meta.state_choices)
    order = forms.ChoiceField(choices=Meta.order_choices)
    order_by = forms.ChoiceField(choices=Meta.order_by_choices)
        # widgets = {
        #     'search': forms.TextInput(required=False, attrs={
        #         'class': 'form-control',
        #     }),
        #     'priority': forms.ChoiceField(choices=priority_choices, required=False, attrs={
        #         'class': 'form-select',
        #     }),
        #     'state': forms.ChoiceField(choices=state_choices, required=False, attrs={
        #         'class': 'form-select',
        #     }),
        #     'order': forms.ChoiceField(choices=order_choices, required=False, attrs={
        #         'class': 'form-select',
        #     }),
        #     'order_by': forms.ChoiceField(choices=order_by_choices, required=False, attrs={
        #         'class': 'form-select',
        #     }),
        # }

    def __init__(self, *args, **kwargs):
        super(TicketFilterForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].required = False
        self.fields['search'].widget.attrs['class'] = 'form-control'
        self.fields['priority'].widget.attrs['class'] = 'form-select'
        self.fields['state'].widget.attrs['class'] = 'form-select'
        self.fields['order'].widget.attrs['class'] = 'form-select'
        self.fields['order_by'].widget.attrs['class'] = 'form-select'