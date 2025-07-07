from django.urls import path, include
from rest_framework import routers

from planetarium.views import ShowThemeViewSet, AstronomyShowViewSet


app_name = "planetarium"

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)
router.register("astronomy-shows", AstronomyShowViewSet)


urlpatterns = [
    path("", include(router.urls)),

]