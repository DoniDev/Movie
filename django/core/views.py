from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import VoteForm, MovieImageForm
from .models import Movie, Person, Role
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Vote
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.core.exceptions import (
    PermissionDenied,
)
from django.http import HttpResponse


class MovieList(ListView):
    model = Movie
    paginate_by = 10


class MovieDetail(DetailView):
    # model = Movie
    queryset = (
        Movie.objects.all_with_related_persons_score()
    )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user,
            )
            if vote.id:
                vote_form_url = reverse('core:UpdateVote', kwargs={'movie_id': vote.movie.id, 'pk': vote.id})
            else:
                vote_form_url = reverse('core:CreateVote', kwargs={'movie_id': self.object.id})

            likes = self.object.vote_set.all().filter(value=1).count()
            dislikes = self.object.vote_set.all().filter(value=-1).count()

            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
            ctx['likes'] = likes
            ctx['dislikes'] = dislikes
            ctx['image_form'] = self.movie_image_form

        return ctx

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(
            queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied(
                'cannot change another '
                'users vote')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse(
            'core:MovieDetail',
            kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse(
            'core:MovieDetail',
            kwargs={'pk': movie_id})
        return redirect(
            to=movie_detail_url)


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm
    # model = Vote

    # used to pre-populate a form with initial values before form get data values from the request
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs[
            'movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse(
            'core:MovieDetail',
            kwargs={
                'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse(
            'core:MovieDetail',
            kwargs={'pk': movie_id})
        return redirect(
            to=movie_detail_url)




class MovieUploadView(LoginRequiredMixin, CreateView):
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={"pk": movie_id})
        return movie_detail_url




