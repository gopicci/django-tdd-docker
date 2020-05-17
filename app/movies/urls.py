from django.urls import path, include
from .views import MovieList, MovieDetail, MovieViewSet

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet, 'movies')


urlpatterns = [
    # refactoring to use routers
    # path('api/movies/', MovieList.as_view()),
    # path('api/movies/<int:pk>/', MovieDetail.as_view()),
    path('api/', include(router.urls)),
]
