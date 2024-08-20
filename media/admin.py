from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from media.models import User, Genre, Movie, Anime, Cartoon, Series


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "year_released"]
    list_filter = ["year_released"]
    search_fields = ["title"]


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ["title", "year_released", "seasons", "episodes"]
    list_filter = ["year_released", "seasons", "episodes"]
    search_fields = ["title"]


@admin.register(Cartoon)
class CartoonAdmin(admin.ModelAdmin):
    list_display = ["title", "year_released", "seasons", "episodes"]
    list_filter = ["year_released", "seasons", "episodes"]
    search_fields = ["title"]


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ["title", "year_released", "seasons", "episodes"]
    list_filter = ["year_released", "seasons", "episodes"]
    search_fields = ["title"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(User, UserAdmin)
