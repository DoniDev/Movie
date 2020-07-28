from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from uuid import uuid4
from django.conf import settings


class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'acting_credits',
            'role_set__movie',
        )


class Person(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    # objects = Manager()

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        if self.died:
            return '{} {} ({} - {})'.format(self.last_name, self.first_name, self.born, self.died)

        return '{} {} {}'.format(self.last_name, self.first_name, self.born)

    def get_absolute_url(self):
        return reverse('core:PersonDetail', kwargs={'pk': self.id})


class Role(models.Model):
    movie = models.ForeignKey(to='Movie', on_delete=models.DO_NOTHING)
    person = models.ForeignKey(to='Person', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)

    def __str__(self):
        return '{} {} {}'.format(self.movie.id, self.person.id, self.name)

    class Meta:
        unique_together = (
            'movie',
            'person',
            'name'
        )


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related(
            'director'
        )
        qs = qs.prefetch_related(
            'writers', 'actors'
        )
        return qs

    def all_with_related_persons_score(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum('vote__value'))
        return qs

    # def get_the_number_of_likes(self):
    #     qs = self.all_with_related_persons().filter(vote__value=1).count()
    #     return qs
    #
    # def get_the_number_of_dislikes(self):
    #     qs = self.all_with_related_persons().filter(vote__value=-1).count()
    #     return qs


# table name in database => <app_name>_<model_name>
class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audiences'),
        (RATED_PG, 'PG - Parental Guidance'),
        (RATED_R, 'R - Restricted'),
    )
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(to='Person', related_name='directed', on_delete=models.SET_NULL, null=True, blank=True)
    writers = models.ManyToManyField(to='Person', blank=True, related_name='writing_credits')
    actors = models.ManyToManyField(to='Person', through='Role', related_name='acting_credits', blank=True)

    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title')

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

    def get_absolute_url(self):
        return reverse('core:MovieDetail', args=[self.id])


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(movie=movie, user=user)
        except Vote.DoesNotExist:
            return Vote(movie=movie, user=user)


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, 'Like'),
        (DOWN, 'Dislike')
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    def __str__(self):
        return '{} {} {}'.format(self.value, self.user, self.movie.title)

    class Meta:
        unique_together = ('user', 'movie')



def movie_directory_path_with_uuid(instance, filename):
    return '{}/{}'.format(instance.movie.id, uuid4())


class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)





