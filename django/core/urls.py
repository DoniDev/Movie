from django.urls import path
from . views import (
    MovieList,
    MovieDetail,
)

app_name = 'core'
urlpatterns = [
    path('movies/',MovieList.as_view(), name='MovieList'),
    path('movie/<int:pk>/', MovieDetail.as_view(), name='MovieDetail'),

]
