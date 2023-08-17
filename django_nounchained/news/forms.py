from django import forms
from .models import News
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content"]


class SignUpForm(UserCreationForm):
    CHOICES = [
        ('moderator', True),
        ('default', False),
    ]

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    moderator = forms.ChoiceField(choices=CHOICES, initial='default')

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "moderator",
        ]