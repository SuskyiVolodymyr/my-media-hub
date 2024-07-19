from django.urls import reverse

from media.models import UserMovieData, UserAnimeData, Movie, Genre, Anime
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


class MediaListView(TestBaseSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.movie_list_url = reverse("media:movie-list")
        self.new_genre1 = Genre.objects.create(name="Test_genre1")
        self.new_genre2 = Genre.objects.create(name="Test_genre2")
        for i in range(1, 6):
            movie = Movie.objects.get(id=i)
            if i < 4:
                movie.genre.add(self.new_genre1)
            else:
                movie.genre.add(self.new_genre2)

    def test_media_search_form(self):
        res = self.client.get(self.movie_list_url, {"title": "1"})
        search_form = res.context.get('search_form')
        if not search_form:
            self.fail("Search form is not in the context")
        self.assertTrue(search_form.is_valid(), msg=f"Errors: {search_form.errors}")
        expected_movies = Movie.objects.filter(title__icontains="1")
        self.assertQuerysetEqual(
            res.context["object_list"],
            expected_movies
        )

    def test_media_filter_form(self):
        res = self.client.get(
            self.movie_list_url,
            {"genres": [self.new_genre1.id, self.new_genre2.id]}
        )
        filter_form = res.context.get('filter_form')
        if not filter_form:
            self.fail("Search form is not in the context")
        self.assertTrue(filter_form.is_valid(), msg=f"Errors: {filter_form.errors}")
        self.assertEqual(len(res.context["object_list"]), 5)

    def test_movie_order_form_by_title(self):
        res = self.client.get(self.movie_list_url, {"order": "title"})
        order_form = res.context.get('order_form')
        if not order_form:
            self.fail("Search form is not in the context")
        self.assertTrue(order_form.is_valid(), msg=f"Errors: {order_form.errors}")
        self.assertQuerysetEqual(
            res.context["object_list"],
            Movie.objects.order_by("title")
        )

    def test_movie_order_form_by_year_released(self):
        res = self.client.get(self.movie_list_url, {"order": "-year_released"})
        self.assertQuerysetEqual(
            res.context["object_list"],
            Movie.objects.order_by("-year_released")
        )

    def test_media_order_form_by_seasons_and_episodes(self):
        for i in range(1, 10):
            anime = Anime.objects.get(id=1)
            anime.seasons = i % 3
            anime.episodes = i % 2
            anime.save()
        res = self.client.get(reverse("media:anime-list"), {"order": "-seasons"})
        self.assertQuerysetEqual(
            res.context["object_list"],
            Anime.objects.order_by("-seasons")
        )
        res = self.client.get(reverse("media:anime-list"), {"order": "-episodes"})
        self.assertQuerysetEqual(
            res.context["object_list"],
            Anime.objects.order_by("-episodes")
        )

    def test_all_filters_togather(self):
        new_movie = Movie.objects.create(title="Test_111", year_released=2024)
        new_movie.genre.add(self.new_genre1)
        res = self.client.get(
            self.movie_list_url,
            {
                "title": "1",
                "genres": [self.new_genre1.id, self.new_genre2.id],
                "order": "-year_released"
            }
        )
        self.assertQuerysetEqual(
            res.context["object_list"],
            Movie.objects.filter(title__icontains="1").order_by("-year_released")
        )
        self.assertEqual(len(res.context["object_list"]), 2)

    def test_add_media_to_user_list(self):
        self.client.get(reverse("media:movie-add", kwargs={"pk": 1}))
        movie = Movie.objects.get(id=1)
        self.assertNotIn(self.user, movie.user.all())
        self.client.get(reverse("media:movie-add", kwargs={"pk": 1}))
        self.assertIn(self.user, movie.user.all())


