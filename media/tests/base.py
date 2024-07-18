from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from media.models import Movie, Anime, Series, Cartoon


class TestBaseSetUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="Test_user",
            password="Test_user_password"
        )
        for i in range(10):
            movie = Movie.objects.create(
                title=f"Test{i}",
            )
            self.user.movies.add(movie)
        for i in range(9):
            anime = Anime.objects.create(
                title=f"Test{1}",
            )
            self.user.anime.add(anime)
        for i in range(8):
            series = Series.objects.create(
                title=f"Test{i}",
            )
            self.user.series.add(series)
        for i in range(7):
            cartoon = Cartoon.objects.create(
                title=f"Test{i}",
            )
            self.user.cartoons.add(cartoon)
