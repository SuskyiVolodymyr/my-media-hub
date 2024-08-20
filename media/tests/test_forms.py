from django.test import TestCase

from media.forms import UserMovieDataForm, UserAnimeDataForm, UserCartoonDataForm, UserSeriesDataForm, \
    NewUserCreationForm


class TestUserMediaDataForm(TestCase):
    def test_user_movie_data_form(self):
        for rate in range(-9, 9):
            form_data = {
                "rate": rate,
                "status": "1",
                "comment": "test"
            }
            form = UserMovieDataForm(data=form_data)
            if not 0 <= rate <= 5:
                self.assertFalse(form.is_valid())
                self.assertEqual(form.errors["__all__"], ["Rate must be between 0 and 5"])
            else:
                self.assertTrue(form.is_valid())

    def test_user_anime_data_form(self):
        for rate in range(-9, 9):
            form_data = {
                "rate": rate,
                "status": "1",
                "comment": "test",
            }
            form = UserAnimeDataForm(data=form_data)
            if not 0 <= rate <= 5:
                self.assertFalse(form.is_valid())
                self.assertEqual(form.errors["__all__"], ["Rate must be between 0 and 5"])
            else:
                self.assertTrue(form.is_valid())

    def test_user_cartoon_data_form(self):
        for rate in range(-9, 9):
            form_data = {
                "rate": rate,
                "status": "1",
                "comment": "test",
            }
            form = UserCartoonDataForm(data=form_data)
            if not 0 <= rate <= 5:
                self.assertFalse(form.is_valid())
                self.assertEqual(form.errors["__all__"], ["Rate must be between 0 and 5"])
            else:
                self.assertTrue(form.is_valid())

    def test_user_series_data_form(self):
        for rate in range(-9, 9):
            form_data = {
                "rate": rate,
                "status": "1",
                "comment": "test",
            }
            form = UserSeriesDataForm(data=form_data)
            if not 0 <= rate <= 5:
                self.assertFalse(form.is_valid())
                self.assertEqual(form.errors["__all__"], ["Rate must be between 0 and 5"])
            else:
                self.assertTrue(form.is_valid())


class TestUserCreationForm(TestCase):
    def setUp(self):
        self.form = NewUserCreationForm()

    def test_registration_form_fields(self):
        self.assertIn("username", self.form.fields)
        self.assertIn("email", self.form.fields)
        self.assertIn("password1", self.form.fields)
        self.assertIn("password2", self.form.fields)
