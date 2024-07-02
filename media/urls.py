from django.urls import path

from media.views import (
    index,
    UserCreateView,
    UserMovieListView,
    UserAnimeListView,
    MovieListView,
    MovieCreateView,
    MovieDetailView,
    MovieUpdateView,
    MovieDeleteView,
    add_movie,
    AnimeListView,
    AnimeCreateView,
    AnimeDetailView,
    AnimeUpdateView,
    AnimeDeleteView,
    add_anime,
    update_user_movie_data_view,
    update_user_anime_data_view,
)

urlpatterns = [
    path("", index, name="index"),
    path("user/create", UserCreateView.as_view(), name="user-create"),
    path("user_movies/", UserMovieListView.as_view(), name="user-movie-list"),
    path("user_anime/", UserAnimeListView.as_view(), name="user-anime-list"),
    path("user_movie_data/<int:pk>/update/", update_user_movie_data_view, name="user-movie-data-update"),
    path("user_anime_data/<int:pk>/update/", update_user_anime_data_view, name="user-anime-data-update"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:pk>/add_movie", add_movie, name="movie-add"),
    path("movie/create", MovieCreateView.as_view(), name="movie-create"),
    path("movie/<int:pk>/detail/", MovieDetailView.as_view(), name="movie-detail"),
    path("movie/<int:pk>/update/", MovieUpdateView.as_view(), name="movie-update"),
    path("movie/<int:pk>/delete", MovieDeleteView.as_view(), name="movie-delete"),
    path("anime/", AnimeListView.as_view(), name="anime-list"),
    path("anime/<int:pk>/add_anime", add_anime, name="anime-add"),
    path("anime/create", AnimeCreateView.as_view(), name="anime-create"),
    path("anime/<int:pk>/detail", AnimeDetailView.as_view(), name="anime-detail"),
    path("anime/<int:pk>/update/", AnimeUpdateView.as_view(), name="anime-update"),
    path("anime/<int:pk>/delete", AnimeDeleteView.as_view(), name="anime-delete"),

]

app_name = "media"
