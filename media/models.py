from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class UserMediaDataMixin:
    rate = models.DecimalField(null=True)
    status = models.CharField(choices=["watching", "want to watch", "dropped", "finished"])
    comment = models.TextField()


class UserMovieData(models.Model, UserMediaDataMixin):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)


class UserAnimeData(models.Model, UserMediaDataMixin):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    anime = models.ForeignKey("Anime", on_delete=models.CASCADE)


class UserCartoonData(models.Model, UserMediaDataMixin):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    cartoon = models.ForeignKey("Cartoon", on_delete=models.CASCADE)


class UserSeriesData(models.Model, UserMediaDataMixin):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    series = models.ForeignKey("Series", on_delete=models.CASCADE)


class Genre(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name="movies")
    year_released = models.IntegerField(null=True)
    user = models.ManyToManyField(get_user_model(), through=UserMovieData, related_name="movies")

    class Meta:
        ordering = ("title", )

    def __str__(self):
        return self.title


class Series(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name="series")
    seasons = models.IntegerField(null=True)
    episodes = models.IntegerField(null=True)
    year_released = models.IntegerField(null=True)
    user = models.ManyToManyField(get_user_model(), through=UserSeriesData, related_name="series")

    class Meta:
        ordering = ("title", )
        verbose_name_plural = "series"

    def __str__(self):
        return self.title


class Anime(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name="anime")
    seasons = models.IntegerField(null=True)
    episodes = models.IntegerField(null=True)
    year_released = models.IntegerField(null=True)
    user = models.ManyToManyField(get_user_model(), through=UserAnimeData, related_name="anime")

    class Meta:
        ordering = ("title", )
        verbose_name_plural = "anime"

    def __str__(self):
        return self.title


class Cartoon(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name="cartoons")
    seasons = models.IntegerField(null=True)
    episodes = models.IntegerField(null=True)
    year_released = models.IntegerField(null=True)
    user = models.ManyToManyField(get_user_model(), through=UserCartoonData, related_name="cartoons")

    class Meta:
        ordering = ("title", )

    def __str__(self):
        return self.title
