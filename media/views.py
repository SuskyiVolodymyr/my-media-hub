from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from media.forms import UserMovieDataForm
from media.models import Movie, Anime, Series, Cartoon, User, UserMovieData


@login_required
def index(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(id=request.user.id)
    movies = user.movies.count()
    anime = user.anime.count()
    series = user.series.count()
    cartoons = user.cartoons.count()
    context = {
        "movies": movies,
        "anime": anime,
        "series": series,
        "cartoons": cartoons
    }
    return render(request, "media/index.html", context=context)


class UserMovieListView(generic.ListView):
    model = UserMovieData
    paginate_by = 50
    template_name = "media/user_movie_list.html"

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return UserMovieData.objects.filter(user_id=user.id)


class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 50


class MovieDetailView(generic.DetailView):
    model = Movie


@login_required
def update_user_movie_data_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user
    movie = get_object_or_404(Movie, id=pk)
    user_movie_data = get_object_or_404(UserMovieData, user=user, movie=movie)

    if request.method == 'POST':
        form = UserMovieDataForm(request.POST, instance=user_movie_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("media:user-movie-list"))
    else:
        form = UserMovieDataForm(instance=user_movie_data)

    return render(request, 'media/user_movie_data_form.html', {'form': form, 'movie': movie})


def add_movie(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=request.user.id)
    if Movie.objects.get(id=pk) in user.movies.all():
        user.movies.remove(pk)
    else:
        user.movies.add(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy("media:movie-list")))
