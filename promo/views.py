from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from promo.models import Promo
from . import serializers


class PromoViewSet(ModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = serializers.PromoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        return [permissions.IsAdminUser(), ]
