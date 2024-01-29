from django.db import models

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "bio", "email", "locations", "profile_image"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
