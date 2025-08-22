from django import forms
from .models import Keyword, RecordingSchedule

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ['word']
        widgets = {
            'word': forms.TextInput(attrs={
                'placeholder': 'Enter keyword to monitor (e.g., Tesla, Apple)',
                'class': 'form-control'
            })
        }