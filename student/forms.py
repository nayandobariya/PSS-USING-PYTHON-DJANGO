from django import forms
from django.contrib.auth.models import User
from . import models


class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(StudentUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False


class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['address','mobile','profile_pic']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False
        self.fields['address'].required = True
        self.fields['mobile'].required = True
