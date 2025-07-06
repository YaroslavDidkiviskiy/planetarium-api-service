from django.urls import path, include
from rest_framework import routers

from planetarium.views import ShowThemeViewSet


app_name = "planetarium"

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)


urlpatterns = [
    path("", include(router.urls)),

]