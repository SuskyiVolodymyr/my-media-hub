from abc import ABC

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from media.models import UserMovieData, Genre, UserAnimeData, UserSeriesData


class UserMediaDataForm(forms.ModelForm):
    rate = forms.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False
    )

    def clean_rate(self):
        rate = self.cleaned_data["rate"]
        if rate is not None and not 0 <= rate <= 5:
            raise forms.ValidationError("Rate must be between 0 and 5")

        return rate


class UserMovieDataForm(UserMediaDataForm):
    class Meta:
        model = UserMovieData
        fields = ["rate", "status", "comment"]


class UserAnimeDataForm(UserMediaDataForm):
    class Meta:
        model = UserAnimeData
        fields = ["rate", "status", "comment"]


class UserSeriesDataForm(UserMediaDataForm):
    class Meta:
        model = UserSeriesData
        fields = ["rate", "status", "comment"]


class NewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
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


class StatusFilterForm(forms.Form):
    show_only = forms.ChoiceField(
        choices=(
            ("", "All"),
            ("1", "Watching"),
            ("2", "Want to watch"),
            ("3", "Dropped"),
            ("4", "Finished"),
        ),
        required=False,
        label="show only",
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


class MediaOrderForm(forms.Form):
    order = forms.ChoiceField(
        choices=(
            ("title", "Title"),
            ("-year_released", "Year"),
            ("-seasons", "Seasons"),
            ("-episodes", "Episodes")
        ),
        required=False,
        label="Sort by",
    )
