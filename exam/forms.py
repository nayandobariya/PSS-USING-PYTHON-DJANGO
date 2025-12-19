from django import forms
from django.contrib.auth.models import User
from . import models


class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name']

class QuestionForm(forms.ModelForm):

    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'option1': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'option2': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'option3': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'option4': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username or Email")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")

class StudentCSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File", help_text="CSV should have columns: first_name, last_name, username, password, email, address, mobile")
