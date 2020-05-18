from django.urls import include, path
from rest_framework import routers

# from .views import MovieList, MovieDetail
from .views import MovieViewSet

router = routers.SimpleRouter()
router.register(r"movies", MovieViewSet, "movies")


urlpatterns = [
    # refactoring to use routers
    # path('api/movies/', MovieList.as_view()),
    # path('api/movies/<int:pk>/', MovieDetail.as_view()),
    path("api/", include(router.urls)),
]
