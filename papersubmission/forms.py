from django import forms
from .models import TheoryPaper

class PaperUploadForm(forms.ModelForm):
    class Meta:
        model = TheoryPaper
        fields = ['course', 'paper_file']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'paper_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
