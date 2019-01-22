from django import forms
from django.contrib.auth.models import User
from mysite.models  import Deck, Topic, Post, ProfaneWord
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        help_texts = {
            'username': None,
            'email': None,
            'password1': "test",
            'password2': "test",
        }
        fields = ['username', 'email', 'password1', 'password2']


class TopicForm(forms.ModelForm):

    title = forms.CharField(max_length=60, required=True)

    class Meta():
        model = Topic
        exclude = ('creator','updated', 'created', 'closed', 'forum',)


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        exclude = ('creator', 'updated', 'created','topic', 'user_ip',)