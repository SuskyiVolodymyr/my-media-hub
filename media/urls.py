from django.urls import path

from media.views import (
    index,
    UserMovieListView,
    MovieListView,
    add_movie,
    MovieDetailView,
    update_user_movie_data_view,
    MovieUpdateView,
    MovieCreateView,
    UserCreateView, MovieDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("user_movies/", UserMovieListView.as_view(), name="user-movie-list"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:pk>/add_movie", add_movie, name="movie-add"),
    path("user_movie_data/<int:pk>/update/", update_user_movie_data_view, name="user-movie-data-update"),
    path("movie/<int:pk>/detail/", MovieDetailView.as_view(), name="movie-detail"),
    path("movie/<int:pk>/update/", MovieUpdateView.as_view(), name="movie-update"),
    path("movie/create", MovieCreateView.as_view(), name="movie-create"),
    path("movie/<int:pk>/delete", MovieDeleteView.as_view(), name="movie-delete"),
    path("user/create", UserCreateView.as_view(), name="user-create"),

]

app_name = "media"
