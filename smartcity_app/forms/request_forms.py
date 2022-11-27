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
            self.fields['ticketid'].initial = ticket_choices[ticket_id]

        tech_choices = [('', '-----------')]
        technicians = User.objects.filter(role='Technician').all()
        for tech in technicians:
            tech_choices.append(tuple((tech.id, '(#' + f'{tech.id}' + ') ' + tech.name + ' ' + tech.surname)))

        self.fields['technicianid'].widget.choices = tech_choices
        self.fields['technicianid'].widget.attrs['class'] = 'form-select'


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

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = ServiceRequestComments
#         fields = ['text']
#         widgets = {
#             'text' : forms.Textarea(attrs={
#                 'class':'form-control',
#                 'rows' : '3'
#             }),
#         }