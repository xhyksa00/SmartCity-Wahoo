from django import forms
from ..models import ServiceRequest, ServiceRequestComments, User, Ticket

PRIORITY_CHOICES = [
    ('Lowest', 'Lowest'),
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Highest', 'Highest'),
]

class CreateRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['description', 'priority', 'ticketid', 'technicianid']
        widgets = {
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

        technicianid = forms.ChoiceField()
        ticketid = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        ticket_id = kwargs.pop('tid', None)
        super(CreateRequestForm, self).__init__(*args, **kwargs)

        ticket_choices = [('', '-----------')]
        tickets = Ticket.objects.filter(state='Open').all()
        for ticket in tickets:
            ticket_choices.append(tuple((ticket.id, '(#' + f'{ticket.id}' + ') ' + ticket.title)))
        
        self.fields['ticketid'].widget.choices = ticket_choices
        self.fields['ticketid'].widget.attrs['class'] = 'form-select'

        if ticket_id:
            for choice in ticket_choices:
                if choice[0] == ticket_id:
                    self.fields['ticketid'].initial = choice

        tech_choices = [('', '-----------')]
        technicians = User.objects.filter(role='Technician').all()
        for tech in technicians:
            tech_choices.append(tuple((tech.id, '(#' + f'{tech.id}' + ') ' + tech.name + ' ' + tech.surname)))

        self.fields['technicianid'].widget.choices = tech_choices
        self.fields['technicianid'].widget.attrs['class'] = 'form-select'

class PriorityForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['priority']

    priority = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(PriorityForm, self).__init__(*args, **kwargs)
        choices = [('Lowest','Lowest'),('Low','Low'),('Medium','Medium'),('High','High'),('Highest','Highest')]

        self.fields['priority'].widget.choices = choices
        self.fields['priority'].widget.required = False
        self.fields['priority'].widget.attrs['onchange'] = 'this.form.submit()'

class EstimatedPriceForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['price']

    price = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(EstimatedPriceForm, self).__init__(*args, **kwargs)

        self.fields['price'].widget.required = False
        self.fields['price'].widget.attrs['onchange'] = 'this.form.submit()'

class ExpectedDateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['days_remaining']

    days_remaining = forms.DateInput()

    def __init__(self, *args, **kwargs):
        super(ExpectedDateForm, self).__init__(*args, **kwargs)

        self.fields['days_remaining'].widget.required = False
        # self.fields['days_remaining'].widget = forms.DateInput()
        self.fields['days_remaining'].widget.attrs['onchange'] = 'this.form.submit()'
        self.fields['days_remaining'].widget.attrs['type'] = 'date'


class AssignTechnicianForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['technicianid']
        
    technicianid = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(AssignTechnicianForm, self).__init__(*args, **kwargs)
        
        choices = [('', '-----------')]
        technicnains = User.objects.filter(role='Technician').all()
        for tech in technicnains:
            choices.append(tuple((tech.id, '(#' + f'{tech.id}' + ') ' + tech.name + ' ' + tech.surname)))

        self.fields['technicianid'].widget.choices = choices
        self.fields['technicianid'].widget.required = False
        self.fields['technicianid'].widget.attrs['onchange'] = 'this.form.submit()'

class ServiceRCommentForm(forms.ModelForm):
    class Meta:
        model = ServiceRequestComments
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={
                'class':'form-control',
                'rows' : '3'
            }),
        }

class RequestFilterForm(forms.Form):
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
            ('ticketid__title', 'Relevant Ticket'),
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
        super(RequestFilterForm, self).__init__(*args, **kwargs)
        for fieldName in self.Meta.fields:
            self.fields[fieldName].required = False
        self.fields['search'].widget.attrs['class'] = 'form-control'
        self.fields['search'].widget.attrs['placeholder'] = 'Search Relevant Ticekt titles and Request descriptions'
        self.fields['priority'].widget.attrs['class'] = 'form-select'
        self.fields['state'].widget.attrs['class'] = 'form-select'
        self.fields['order'].widget.attrs['class'] = 'form-select'
        self.fields['order_by'].widget.attrs['class'] = 'form-select'
