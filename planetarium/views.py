from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from planetarium.models import ShowTheme
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import ShowThemeSerializer


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    authentication_classes = (JWTAuthentication,)
