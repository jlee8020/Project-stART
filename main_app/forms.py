from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Comment, Profile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['content']