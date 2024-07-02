from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from media.forms import UserMovieDataForm, NewUserCreationForm, MediaSearchForm, MediaFilterForm, MovieOrderForm, \
    AnimeOrderForm, UserAnimeDataForm
from media.models import Movie, Anime, Series, Cartoon, User, UserMovieData, Genre, UserAnimeData


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


class UserCreateView(generic.CreateView):
    form_class = NewUserCreationForm
    template_name = "registration/user_form.html"
    success_url = reverse_lazy("media:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            messages.error(self.request, 'There was a problem logging you in. Please try again.')
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            'There was an error with your submission. Please check the form and try again.'
        )
        return super().form_invalid(form)


class UserMovieListView(generic.ListView, LoginRequiredMixin):
    model = UserMovieData
    paginate_by = 50
    template_name = "media/user_movie_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = MediaSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        queryset = UserMovieData.objects.filter(user_id=user.id)
        form = MediaSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                movie__title__icontains=form.cleaned_data["title"]
            )
        return queryset


class UserAnimeListView(generic.ListView, LoginRequiredMixin):
    model = UserAnimeData
    paginate_by = 50
    template_name = "media/user_anime_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = MediaSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        queryset = UserAnimeData.objects.filter(user_id=user.id)
        form = MediaSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                anime__title__icontains=form.cleaned_data["title"]
            )
        return queryset


class MovieListView(generic.ListView, LoginRequiredMixin):
    model = Movie
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = MediaSearchForm(self.request.GET)
        filter_form = MediaFilterForm(self.request.GET)
        order_form = MovieOrderForm(self.request.GET)
        context["search_form"] = search_form
        context["filter_form"] = filter_form
        context["order_form"] = order_form
        context["genres"] = Genre.objects.all()
        context["selected_genres"] = self.request.GET.getlist("genres")
        return context

    def get_queryset(self):
        queryset = Movie.objects.prefetch_related("genre")
        search_form = MediaSearchForm(self.request.GET)
        filter_form = MediaFilterForm(self.request.GET)
        order_form = MovieOrderForm(self.request.GET)

        if search_form.is_valid():
            title = search_form.cleaned_data.get("title", "")
            if title:
                queryset = queryset.filter(
                    title__icontains=title
                )
        if filter_form.is_valid():
            selected_genres = filter_form.cleaned_data.get("genres", [])
            if selected_genres:
                queryset = queryset.filter(genre__in=selected_genres).distinct()

        if order_form.is_valid():
            order = order_form.cleaned_data.get("order", "title")
            if order:
                queryset = queryset.order_by(order)

        return queryset


class AnimeListView(generic.ListView, LoginRequiredMixin):
    model = Anime
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = MediaSearchForm(self.request.GET)
        filter_form = MediaFilterForm(self.request.GET)
        order_form = AnimeOrderForm(self.request.GET)
        context["search_form"] = search_form
        context["filter_form"] = filter_form
        context["order_form"] = order_form
        context["genres"] = Genre.objects.all()
        context["selected_genres"] = self.request.GET.getlist("genres")
        return context

    def get_queryset(self):
        queryset = Anime.objects.prefetch_related("genre")
        search_form = MediaSearchForm(self.request.GET)
        filter_form = MediaFilterForm(self.request.GET)
        order_form = AnimeOrderForm(self.request.GET)

        if search_form.is_valid():
            title = search_form.cleaned_data.get("title", "")
            if title:
                queryset = queryset.filter(
                    title__icontains=title
                )
        if filter_form.is_valid():
            selected_genres = filter_form.cleaned_data.get("genres", [])
            if selected_genres:
                queryset = queryset.filter(genre__in=selected_genres).distinct()

        if order_form.is_valid():
            order = order_form.cleaned_data.get("order", "title")
            if order:
                queryset = queryset.order_by(order)

        return queryset


class MovieDetailView(generic.DetailView, LoginRequiredMixin):
    model = Movie


class AnimeDetailView(generic.DetailView, LoginRequiredMixin):
    model = Anime


class MovieUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Movie
    fields = ["year_released", "description", "genre"]

    def get_success_url(self):
        movie_id = self.object.id
        return reverse_lazy("media:movie-detail", kwargs={"pk": movie_id})


class AnimeUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Anime
    fields = ["year_released", "description", "genre", "seasons", "episodes"]

    def get_success_url(self):
        anime_id = self.object.id
        return reverse_lazy("media:anime-detail", kwargs={"pk": anime_id})


class MovieCreateView(generic.CreateView, LoginRequiredMixin):
    model = Movie
    fields = ["title", "year_released", "description", "genre"]

    def get_success_url(self):
        movie_id = self.object.id
        return reverse_lazy("media:movie-detail", kwargs={"pk": movie_id})


class AnimeCreateView(generic.CreateView, LoginRequiredMixin):
    model = Anime
    fields = ["title", "year_released", "description", "genre", "seasons", "episodes"]

    def get_success_url(self):
        anime_id = self.object.id
        return reverse_lazy("media:anime-detail", kwargs={"pk": anime_id})


class MovieDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Movie
    success_url = reverse_lazy("media:movie-list")


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


@login_required
def update_user_anime_data_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = request.user
    anime = get_object_or_404(Anime, id=pk)
    user_anime_data = get_object_or_404(UserAnimeData, user=user, anime=anime)

    if request.method == 'POST':
        form = UserAnimeDataForm(request.POST, instance=user_anime_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("media:user-anime-list"))
    else:
        form = UserAnimeDataForm(instance=user_anime_data)

    return render(request, 'media/user_anime_data_form.html', {'form': form, 'anime': anime})


@login_required
def add_movie(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=request.user.id)
    if Movie.objects.get(id=pk) in user.movies.all():
        user.movies.remove(pk)
    else:
        user.movies.add(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy("media:movie-list")))


@login_required
def add_anime(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=request.user.id)
    if Anime.objects.get(id=pk) in user.anime.all():
        user.anime.remove(pk)
    else:
        user.anime.add(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy("media:anime-list")))
