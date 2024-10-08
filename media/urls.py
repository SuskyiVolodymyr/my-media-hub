from media.url_imports import *

urlpatterns = [
    path(
        "",
        index,
        name="index"),
    path(
        "users/create",
        UserCreateView.as_view(),
        name="users-create"),
    path(
        "user_movies/",
        UserMovieListView.as_view(),
        name="user-movies-list"),
    path(
        "user_movies_data/<int:pk>/update/",
        update_user_movie_data_view,
        name="user-movies-data-update"
    ),
    path(
        "movies/",
        MovieListView.as_view(),
        name="movies-list"),
    path(
        "movies/<int:pk>/add_movie",
        add_movie,
        name="movies-add"),
    path(
        "movies/create",
        MovieCreateView.as_view(),
        name="movies-create"),
    path(
        "movies/<int:pk>/detail/",
        MovieDetailView.as_view(),
        name="movies-detail"
    ),
    path(
        "movies/<int:pk>/update/",
        MovieUpdateView.as_view(),
        name="movies-update"
    ),
    path(
        "movies/<int:pk>/delete",
        MovieDeleteView.as_view(),
        name="movies-delete"
    ),
    path(
        "user_anime/",
        UserAnimeListView.as_view(),
        name="user-anime-list"),
    path(
        "user_anime_data/<int:pk>/update/",
        update_user_anime_data_view,
        name="user-anime-data-update"
    ),
    path(
        "anime/",
        AnimeListView.as_view(),
        name="anime-list"
    ),
    path(
        "anime/<int:pk>/add_anime",
        add_anime,
        name="anime-add"
    ),
    path(
        "anime/create",
        AnimeCreateView.as_view(),
        name="anime-create"
    ),
    path(
        "anime/<int:pk>/detail",
        AnimeDetailView.as_view(),
        name="anime-detail"
    ),
    path(
        "anime/<int:pk>/update/",
        AnimeUpdateView.as_view(),
        name="anime-update"
    ),
    path(
        "anime/<int:pk>/delete",
        AnimeDeleteView.as_view(),
        name="anime-delete"
    ),
    path(
        "user_series/",
        UserSeriesListView.as_view(),
        name="user-series-list"
    ),
    path(
        "user_series_data/<int:pk>/update/",
        update_user_series_data_view,
        name="user-series-data-update"
    ),
    path(
        "series/",
        SeriesListView.as_view(),
        name="series-list"
    ),
    path(
        "series/<int:pk>/add_series",
        add_series,
        name="series-add"
    ),
    path(
        "series/create",
        SeriesCreateView.as_view(),
        name="series-create"
    ),
    path(
        "series/<int:pk>/detail",
        SeriesDetailView.as_view(),
        name="series-detail"
    ),
    path(
        "series/<int:pk>/update/",
        SeriesUpdateView.as_view(),
        name="series-update"
    ),
    path(
        "series/<int:pk>/delete",
        SeriesDeleteView.as_view(),
        name="series-delete"
    ),
    path(
        "user_cartoons/",
        UserCartoonListView.as_view(),
        name="user-cartoons-list"
    ),
    path(
        "user_cartoons_data/<int:pk>/update/",
        update_user_cartoon_data_view,
        name="user-cartoons-data-update"
    ),
    path(
        "cartoons/",
        CartoonListView.as_view(),
        name="cartoons-list"
    ),
    path(
        "cartoons/<int:pk>/add_cartoon",
        add_cartoon,
        name="cartoons-add"
    ),
    path(
        "cartoons/create",
        CartoonCreateView.as_view(),
        name="cartoons-create"
    ),
    path(
        "cartoons/<int:pk>/detail",
        CartoonDetailView.as_view(),
        name="cartoons-detail"
    ),
    path(
        "cartoons/<int:pk>/update/",
        CartoonUpdateView.as_view(),
        name="cartoons-update"
    ),
    path(
        "cartoons/<int:pk>/delete",
        CartoonDeleteView.as_view(),
        name="cartoons-delete"
    ),

]

app_name = "media"
