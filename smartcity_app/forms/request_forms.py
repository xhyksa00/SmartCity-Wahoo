from django import forms
from ..models import ServiceRequest, ServiceRequestComments

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
        fields = ['description', 'days_remaining', 'priority', 'ticketid', 'technicianid', 'authorid']
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