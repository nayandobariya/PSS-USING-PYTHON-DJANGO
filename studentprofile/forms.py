from django import forms
from .models import StudentProfileRequest, PaperRequest, Feedback, Paper
from student.models import Student

class StudentProfileRequestForm(forms.ModelForm):
    class Meta:
        model = StudentProfileRequest
        fields = ['first_name', 'middle_name', 'last_name', 'roll_no', 'course']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

class PaperUploadForm(forms.ModelForm):
    selected_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(status=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label="Select Students"
    )
    class Meta:
        model = Paper
        fields = ['course', 'title', 'excel_file']

class PaperRequestForm(forms.ModelForm):
    class Meta:
        model = PaperRequest
        fields = ['paper']
        widgets = {
            'paper': forms.Select(attrs={'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
