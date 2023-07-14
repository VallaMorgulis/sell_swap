from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]

    # @method_decorator(cache_page(60))  # Кеширование на 1 минуту
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
