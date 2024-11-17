# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import  Course, Topic
from ckeditor.fields import RichTextField  # For model definition

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

class TopicForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)  # Ensuring content is required with a Textarea widget

    class Meta:
        model = Topic
        fields = ['name', 'course', 'description', 'content']
