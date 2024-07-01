from django import forms
from django.contrib.auth.forms import UserCreationForm

from media.models import UserMovieData, User, Genre


class UserMovieDataForm(forms.ModelForm):
    class Meta:
        model = UserMovieData
        fields = ["rate", "status", "comment"]


class NewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]


class MovieSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title"
            }
        )
    )


class MovieFilterForm(forms.Form):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=""
    )