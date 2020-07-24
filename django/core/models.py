from django.db import models
from django.urls import reverse


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



