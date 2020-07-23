from django.shortcuts import render
from . models import Movie
from django.views.generic import ListView, DetailView


class MovieList(ListView):
    model = Movie
    paginate_by = 1


class MovieDetail(DetailView):
    model = Movie
