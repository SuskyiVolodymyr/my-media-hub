from django import forms
from django.contrib.auth.forms import UserCreationForm

from media.models import UserMovieData, User, Genre, UserAnimeData


class UserMovieDataForm(forms.ModelForm):
    class Meta:
        model = UserMovieData
        fields = ["rate", "status", "comment"]


class UserAnimeDataForm(forms.ModelForm):
    class Meta:
        model = UserAnimeData
        fields = ["rate", "status", "comment"]


class NewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]


class MediaSearchForm(forms.Form):
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


class MediaFilterForm(forms.Form):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=""
    )


class MovieOrderForm(forms.Form):

    order = forms.ChoiceField(
        choices=(("title", "Title"), ("-year_released", "Year")),
        required=False,
        label="Sort by",
    )


class AnimeOrderForm(forms.Form):

    order = forms.ChoiceField(
        choices=(("title", "Title"), ("-year_released", "Year")),
        required=False,
        label="Sort by",
    )
