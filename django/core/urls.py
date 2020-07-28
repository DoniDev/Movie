from django.urls import path
from .views import (
    MovieList,
    MovieDetail,
    PersonDetail,
    CreateVote,
    UpdateVote,
    MovieUploadView

)
from django.conf import settings
from django.conf.urls.static import  static


app_name = 'core'

urlpatterns = [
    path('movies/', MovieList.as_view(), name='MovieList'),
    path('movie/<int:pk>/', MovieDetail.as_view(), name='MovieDetail'),
    path('movie/<int:movie_id>/vote/', CreateVote.as_view(), name='CreateVote'),
    path('movie/<int:movie_id>/vote/<int:pk>/', UpdateVote.as_view(), name='UpdateVote'),
    path('person/<int:pk>/', PersonDetail.as_view(), name='PersonDetail'),
    path('movie/<int:movie_id>/image/upload/', MovieUploadView.as_view(), name='MovieImageUpload'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

