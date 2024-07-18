from django.urls import reverse

from media.models import UserMovieData, UserAnimeData, Movie
from media.tests.base import TestBaseSetUp


class TestHomePage(TestBaseSetUp):
    def setUp(self):
        super().setUp()
        self.url = reverse("media:index")

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)
        self.assertTemplateUsed(reverse("login"))

    def test_correct_home_page_context(self):
        self.client.force_login(self.user)
        res = self.client.get(self.url)
        self.assertIn("Movies:<br> 10", res.content.decode())
        self.assertIn("Anime:<br> 9", res.content.decode())
        self.assertIn("Series:<br> 8", res.content.decode())
        self.assertIn("Cartoons:<br> 7", res.content.decode())


class TestUserMediaListView(TestBaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.user_movie_url = reverse("media:user-movie-list")
        self.user_anime_url = reverse("media:user-anime-list")
        self.user_series_url = reverse("media:user-series-list")
        self.user_cartoon_url = reverse("media:user-cartoon-list")

    def test_user_media_search_form(self):
        res = self.client.get(self.user_movie_url, {"title": "1"})
        search_form = res.context.get('search_form')
        if not search_form:
            self.fail("Search form is not in the context")
        self.assertTrue(search_form.is_valid(), msg=f"Errors: {search_form.errors}")
        expected_movies = UserMovieData.objects.filter(user=self.user, movie__title__icontains="1")
        self.assertQuerysetEqual(
            res.context["object_list"],
            expected_movies
        )

    def test_media_show_only_form(self):
        user_movie = UserMovieData.objects.get(user_id=1, movie_id=1)
        user_movie.status = "2"
        user_movie.save()
        res = self.client.get(self.user_movie_url, {"show_only": "2"})
        show_only_form = res.context.get('show_only_form')
        if not show_only_form:
            self.fail("Show only form is not in the context")
        self.assertTrue(show_only_form.is_valid(), msg=f"Errors: {show_only_form.errors}")
        expected_movies = UserMovieData.objects.filter(user=self.user, status="2")
        self.assertQuerysetEqual(
            res.context["object_list"],
            expected_movies
        )

    def test_media_search_and_show_only_forms(self):
        user_movie = UserMovieData.objects.get(user_id=1, movie_id=1)
        user_movie.status = "2"
        user_movie.save()
        res = self.client.get(self.user_movie_url, {"search_form": "1", "show_only": "1"})
        expected_movies = UserMovieData.objects.filter(user=self.user, status="1",  movie__title__icontains="1")
        self.assertQuerysetEqual(
            res.context["object_list"],
            expected_movies
        )
