from django import forms
from .models import Document

class NewDocForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Document
        fields = ['subject', 'text']