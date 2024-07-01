from django import forms
from django.contrib.auth.forms import UserCreationForm

from media.models import UserMovieData, User


class UserMovieDataForm(forms.ModelForm):
    class Meta:
        model = UserMovieData
        fields = ["rate", "status", "comment"]


class NewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]
