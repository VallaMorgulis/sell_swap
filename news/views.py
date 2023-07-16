from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .models import News


class StandartResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().order_by('-created_at')
    pagination_class = StandartResultPagination
    serializer_class = serializers.NewsSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]

    @method_decorator(cache_page(60))  # Кеширование на 1 минуту
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
