from django.db import IntegrityError
from bs4 import BeautifulSoup as bs
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from requests import get
# from datetime import datetime
from multiprocessing import Pool

from . import serializers
from .models import News
from .tasks import parsing


# Класс для пагинации результатов
class StandartResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


# Ваш ViewSet для модели News
class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().order_by('-created_at')
    pagination_class = StandartResultPagination
    serializer_class = serializers.NewsSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]

    # Декоратор cache_page для кеширования результатов на 15 минут
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def parse_news(self, request, *args, **kwargs):
        parsing.delay()
        return Response('Parse done')
