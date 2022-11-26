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