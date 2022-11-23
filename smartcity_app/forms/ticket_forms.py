from django import forms
from ..models import Ticket

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