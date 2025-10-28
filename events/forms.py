from django import forms
from .models import Event, Participant, Category
from django.core.exceptions import ValidationError
from datetime import date, datetime

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_date(self):
        d = self.cleaned_data['date']
        # Example validation: disallow events before year 1900
        if d.year < 1900:
            raise ValidationError("Date seems invalid.")
        return d
