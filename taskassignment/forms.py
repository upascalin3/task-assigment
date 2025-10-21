from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, date
from taskassignment.models import *

class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter contributor name',
                'maxlength': '100'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter email address',
                'type': 'email'
            })
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'end_date', 'start', 'is_completed', 'contributor']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter task title',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Enter task description',
                'rows': 4,
                'maxlength': '500'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'type': 'date'
            }),
            'start': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'type': 'datetime-local'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'contributor': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary'
            })
        }
    
    def clean_start(self):
        start = self.cleaned_data.get('start')
        if start:
            now = datetime.now()
            if start < now:
                raise ValidationError('Start date and time cannot be in the past.')
        return start
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start = self.cleaned_data.get('start')
        
        if end_date and start:
            # Convert start datetime to date for comparison
            start_date = start.date()
            if end_date <= start_date:
                raise ValidationError('End date must be after the start date.')
        
        return end_date
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end_date = cleaned_data.get('end_date')
        
        # Additional validation to ensure end date is after start date
        if start and end_date:
            start_date = start.date()
            if end_date <= start_date:
                raise ValidationError('End date must be after the start date.')
        
        return cleaned_data