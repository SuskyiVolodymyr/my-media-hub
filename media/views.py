from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from media.models import Movie, Anime, Series, Cartoon, User


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
