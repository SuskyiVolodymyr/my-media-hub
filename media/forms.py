from django import forms

from media.models import UserMovieData


class UserMovieDataForm(forms.ModelForm):
    class Meta:
        model = UserMovieData
        fields = ["rate", "status", "comment"]
