from django.db import models
from django.forms import ModelForm
from django import forms

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption", "location"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
