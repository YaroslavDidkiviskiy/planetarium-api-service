from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from planetarium.models import ShowTheme, AstronomyShow
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import ShowThemeSerializer, AstronomyShowSerializer


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    authentication_classes = (JWTAuthentication,)


class AstronomyShowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AstronomyShow.objects.prefetch_related("theme")
    serializer_class = AstronomyShowSerializer
    permission_classes = ()

    def get_queryset(self):
        """Retrieve the movies with filters"""
        theme = self.request.query_params.get("theme")

        queryset = self.queryset

        if theme:
            queryset = queryset.filter(theme__name__icontains=theme)

        return queryset.distinct()
