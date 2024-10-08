from abc import ABC, abstractmethod

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Avg
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from media.forms import (
    UserMovieDataForm,
    NewUserCreationForm,
    MediaSearchForm,
    MediaFilterForm,
    MovieOrderForm,
    UserAnimeDataForm,
    StatusFilterForm,
    MediaOrderForm,
    UserSeriesDataForm,
    UserCartoonDataForm,
    MovieForm,
    AnimeForm,
    SeriesForm,
    CartoonForm,
)
from media.models import (
    Movie,
    Anime,
    Series,
    Cartoon,
    UserMovieData,
    Genre,
    UserAnimeData,
    UserSeriesData,
    UserCartoonData,
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    user = get_user_model().objects.get(id=request.user.id)
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


class UserCreateView(generic.CreateView):
    form_class = NewUserCreationForm
    template_name = "registration/user_form.html"
    success_url = reverse_lazy("media:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            messages.error(
                self.request,
                "There was a problem logging you in. "
                "Please try again."
            )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error with your submission. "
            "Please check the form and try again."
        )
        return super().form_invalid(form)


class UserMediaListView(LoginRequiredMixin, generic.ListView, ABC):
    model = None
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = MediaSearchForm(
            self.request.GET
        )
        context["show_only_form"] = StatusFilterForm(
            self.request.GET
        )
        return context

    @staticmethod
    @abstractmethod
    def media_title_filter(queryset: QuerySet, filter_by: str) -> QuerySet:
        pass

    def get_queryset(self):
        user = get_user_model().objects.get(id=self.request.user.id)
        queryset = self.model.objects.filter(
            user_id=user.id
        ).prefetch_related(self.table)
        search_form = MediaSearchForm(self.request.GET)
        status_filter_form = StatusFilterForm(self.request.GET)

        if search_form.is_valid():
            queryset = self.media_title_filter(
                queryset, search_form.cleaned_data["title"]
            )

        if status_filter_form.is_valid():
            if status_filter_form.cleaned_data.get("show_only"):
                queryset = queryset.filter(
                    status=status_filter_form.cleaned_data.get("show_only")
                )
        return queryset


class UserMovieListView(UserMediaListView):
    model = UserMovieData
    template_name = "media/user_movie_list.html"
    table = "movie"

    @staticmethod
    def media_title_filter(queryset: QuerySet, filter_by: str) -> QuerySet:
        return queryset.filter(movie__title__icontains=filter_by)


class UserAnimeListView(UserMediaListView):
    model = UserAnimeData
    template_name = "media/user_anime_list.html"
    table = "anime"

    @staticmethod
    def media_title_filter(queryset: QuerySet, filter_by: str) -> QuerySet:
        return queryset.filter(anime__title__icontains=filter_by)


class UserSeriesListView(UserMediaListView):
    model = UserSeriesData
    template_name = "media/user_series_list.html"
    table = "series"

    @staticmethod
    def media_title_filter(queryset: QuerySet, filter_by: str) -> QuerySet:
        return queryset.filter(series__title__icontains=filter_by)


class UserCartoonListView(UserMediaListView):
    model = UserCartoonData
    template_name = "media/user_cartoon_list.html"
    table = "cartoon"

    @staticmethod
    def media_title_filter(queryset: QuerySet, filter_by: str) -> QuerySet:
        return queryset.filter(cartoon__title__icontains=filter_by)


class MediaListView(LoginRequiredMixin, generic.ListView, ABC):
    model = None
    paginate_by = 50
    order_form = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = MediaSearchForm(self.request.GET)
        filter_form = MediaFilterForm(self.request.GET)
        context["search_form"] = search_form
        context["filter_form"] = filter_form
        context["order_form"] = self.order_form(self.request.GET)
        context["genres"] = Genre.objects.all()
        context["selected_genres"] = self.request.GET.getlist("genres")
        return context

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related("genre")
        search_form = MediaSearchForm(self.request.GET)
        filter_form = MediaFilterForm(self.request.GET)
        order_form = self.order_form(self.request.GET)

        if search_form.is_valid():
            title = search_form.cleaned_data.get("title", "")
            if title:
                queryset = queryset.filter(
                    title__icontains=title
                )
        if filter_form.is_valid():
            selected_genres = filter_form.cleaned_data.get("genres", [])
            if selected_genres:
                queryset = queryset.filter(
                    genre__in=selected_genres
                ).distinct()

        if order_form.is_valid():
            order = order_form.cleaned_data.get("order", "title")
            if order:
                queryset = queryset.order_by(order)

        return queryset


class MovieListView(MediaListView):
    model = Movie
    order_form = MovieOrderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["user_movies"] = self.request.user.movies.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(average_rate=Avg("usermoviedata__rate"))


class AnimeListView(MediaListView):
    model = Anime
    order_form = MediaOrderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["user_anime"] = self.request.user.anime.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(average_rate=Avg("useranimedata__rate"))


class SeriesListView(MediaListView):
    model = Series
    order_form = MediaOrderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["user_series"] = self.request.user.series.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(average_rate=Avg("userseriesdata__rate"))


class CartoonListView(MediaListView):
    model = Cartoon
    order_form = MediaOrderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["user_cartoon"] = self.request.user.cartoons.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(average_rate=Avg("usercartoondata__rate"))


class MovieDetailView(LoginRequiredMixin, generic.DetailView):
    model = Movie


class AnimeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Anime


class SeriesDetailView(LoginRequiredMixin, generic.DetailView):
    model = Series


class CartoonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cartoon


class MovieUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Movie
    form_class = MovieForm

    def get_success_url(self):
        movie_id = self.object.id
        return reverse_lazy("movies-detail", kwargs={"pk": movie_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response


class AnimeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Anime
    form_class = AnimeForm

    def get_success_url(self):
        anime_id = self.object.id
        return reverse_lazy("media:anime-detail", kwargs={"pk": anime_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response


class SeriesUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Series
    form_class = SeriesForm

    def get_success_url(self):
        series_id = self.object.id
        return reverse_lazy("media:series-detail", kwargs={"pk": series_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response


class CartoonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cartoon
    form_class = CartoonForm

    def get_success_url(self):
        cartoon_id = self.object.id
        return reverse_lazy("cartoons-detail", kwargs={"pk": cartoon_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response


class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movie
    form_class = MovieForm

    def get_success_url(self):
        movie_id = self.object.id
        return reverse_lazy("movies-detail", kwargs={"pk": movie_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response

class AnimeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Anime
    form_class = AnimeForm

    def get_success_url(self):
        anime_id = self.object.id
        return reverse_lazy("media:anime-detail", kwargs={"pk": anime_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response


class SeriesCreateView(LoginRequiredMixin, generic.CreateView):
    model = Series
    form_class = SeriesForm

    def get_success_url(self):
        series_id = self.object.id
        return reverse_lazy("media:series-detail", kwargs={"pk": series_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response


class CartoonCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cartoon
    form_class = CartoonForm

    def get_success_url(self):
        cartoon_id = self.object.id
        return reverse_lazy("cartoons-detail", kwargs={"pk": cartoon_id})

    def form_invalid(self, form):
        response = self.render_to_response(self.get_context_data(form=form))
        response.status_code = 400
        return response


class MovieDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Movie
    success_url = reverse_lazy("movies-list")


class AnimeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Anime
    success_url = reverse_lazy("media:anime-list")


class SeriesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Series
    success_url = reverse_lazy("media:series-list")


class CartoonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cartoon
    success_url = reverse_lazy("cartoons-list")


@login_required
def update_user_media_data(
        request: HttpRequest,
        user_media_data: any,
        user_media_data_form: callable,
        response: str,
        template: str,
        context: dict
):
    if request.method == "POST":
        form = user_media_data_form(request.POST, instance=user_media_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(response)
    else:
        form = user_media_data_form(instance=user_media_data)

    return render(request, template, {"form": form, **context})


@login_required
def update_user_movie_data_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user
    movie = get_object_or_404(Movie, id=pk)
    user_movie_data = get_object_or_404(UserMovieData, user=user, movie=movie)
    response = reverse_lazy("user-movies-list")
    template = "media/user_movie_data_form.html"
    return update_user_media_data(
        request=request,
        user_media_data=user_movie_data,
        user_media_data_form=UserMovieDataForm,
        response=response,
        template=template,
        context={"movie": movie}
    )


@login_required
def update_user_anime_data_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user
    anime = get_object_or_404(Anime, id=pk)
    user_anime_data = get_object_or_404(UserAnimeData, user=user, anime=anime)
    response = reverse_lazy("media:user-anime-list")
    template = "media/user_anime_data_form.html"
    return update_user_media_data(
        request=request,
        user_media_data=user_anime_data,
        user_media_data_form=UserAnimeDataForm,
        response=response,
        template=template,
        context={"anime": anime}
    )


@login_required
def update_user_series_data_view(
        request: HttpRequest,
        pk: int
) -> HttpResponse:
    user = request.user
    series = get_object_or_404(Series, id=pk)
    user_series_data = get_object_or_404(
        UserSeriesData,
        user=user,
        series=series
    )
    response = reverse_lazy("media:user-series-list")
    template = "media/user_series_data_form.html"
    return update_user_media_data(
        request=request,
        user_media_data=user_series_data,
        user_media_data_form=UserSeriesDataForm,
        response=response,
        template=template,
        context={"series": series}
    )


def update_user_cartoon_data_view(
        request: HttpRequest,
        pk: int
) -> HttpResponse:
    user = request.user
    cartoon = get_object_or_404(Cartoon, id=pk)
    user_cartoon_data = get_object_or_404(
        UserCartoonData,
        user=user,
        cartoon=cartoon
    )
    response = reverse_lazy("user-cartoons-list")
    template = "media/user_cartoon_data_form.html"
    return update_user_media_data(
        request=request,
        user_media_data=user_cartoon_data,
        user_media_data_form=UserCartoonDataForm,
        response=response,
        template=template,
        context={"cartoon": cartoon}
    )


@login_required
def add_movie(request: HttpRequest, pk: int) -> HttpResponse:
    user = get_user_model().objects.get(id=request.user.id)
    if Movie.objects.get(id=pk) in user.movies.all():
        user.movies.remove(pk)
    else:
        user.movies.add(pk)
    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse_lazy("movies-list")
        )
    )


@login_required
def add_anime(request: HttpRequest, pk: int) -> HttpResponse:
    user = get_user_model().objects.get(id=request.user.id)
    if Anime.objects.get(id=pk) in user.anime.all():
        user.anime.remove(pk)
    else:
        user.anime.add(pk)
    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse_lazy("media:anime-list")
        )
    )


@login_required
def add_series(request: HttpRequest, pk: int) -> HttpResponse:
    user = get_user_model().objects.get(id=request.user.id)
    if Series.objects.get(id=pk) in user.series.all():
        user.series.remove(pk)
    else:
        user.series.add(pk)
    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse_lazy("media:series-list")
        )
    )


@login_required
def add_cartoon(request: HttpRequest, pk: int) -> HttpResponse:
    user = get_user_model().objects.get(id=request.user.id)
    if Cartoon.objects.get(id=pk) in user.cartoons.all():
        user.cartoons.remove(pk)
    else:
        user.cartoons.add(pk)
    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse_lazy("cartoons-list")
        )
    )
