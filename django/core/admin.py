from django.contrib import admin
from . models import Movie, Person, Role, Vote


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'runtime', 'year']


admin.site.register(Person)
admin.site.register(Role)
admin.site.register(Vote)

