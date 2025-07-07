from django.urls import path, include
from rest_framework import routers

from planetarium.views import ShowThemeViewSet, AstronomyShowViewSet, PlanetariumDomeViewSet, ShowSessionViewSet


app_name = "planetarium"

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)
router.register("astronomy-shows", AstronomyShowViewSet)
router.register("planetarium-domes", PlanetariumDomeViewSet)
router.register("show-sessions", ShowSessionViewSet)


urlpatterns = [
    path("", include(router.urls)),

]