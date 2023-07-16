# Ваш файл views.py

from django.db import IntegrityError
from bs4 import BeautifulSoup as bs
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from requests import get
# from datetime import datetime
# from multiprocessing import Pool

from . import serializers
from .models import News


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
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        # Вызываем функцию для парсинга новостей
        self.parse_news_data()
        return super().list(request, *args, **kwargs)

    # Функция для парсинга новостей и сохранения в базу данных
    def parse_news_data(self):
        url = 'https://www.sport-express.ru/news/'
        html = self.get_html(url)
        soup = self.get_soup(html)
        links = self.get_list_links(soup)
        for link in links:
            self.make_all(link)
        # with Pool(40) as pool:
        #     pool.map(self.make_all, links)

    # Функция для получения HTML контента по URL
    @staticmethod
    def get_html(url: str) -> str:
        response = get(url)
        return response.text

    # Функция для создания объекта BeautifulSoup из HTML
    @staticmethod
    def get_soup(html: str) -> bs:
        return bs(html, 'lxml')

    # Функция для получения списка ссылок на новости
    @staticmethod
    def get_list_links(soup):
        container = soup.find('div', class_='se-news-list-page__items')
        all_news = container.find_all('div', class_='se-news-list-page__item')
        res = []
        count = 0
        for news in all_news:
            if count < 10:
                link = news.find('div', class_='se-material__title se-material__title--size-middle').find('a').get('href')
                res.append(link)
            count += 1
        return res

    # Функция для обработки данных каждой новости
    def make_all(self, link):
        data = self.get_data(link)
        try:
            news = News.objects.create(title=data['title'], image=data['image'], text=data['text'])
        except IntegrityError as e:
            print(f"Запись с title '{data['title']}' уже существует.")
            pass

    # Функция для получения данных из каждой новости
    @staticmethod
    def get_data(link):
        html = NewsViewSet.get_html(link)
        soup = NewsViewSet.get_soup(html)
        container = soup.find('div', class_='se-material-page__body')
        title = container.find('h1', class_='se-material-page__title').text.strip()
        try:
            image = container.find('div', class_='se-photogallery-swipe__image').find('a').find('img').get('src')
        except:
            image = 'No image'
        text = container.find('div', class_='se-material-page__content').find_all('p')
        data = {'title': title, 'image': image, 'text': text}
        return data
