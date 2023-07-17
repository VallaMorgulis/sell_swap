from django.db import IntegrityError
from bs4 import BeautifulSoup as bs
from django.core.management.base import BaseCommand
from requests import get
from datetime import datetime
from multiprocessing import Pool

from news.models import News


def get_html(url: str) -> str:
    response = get(url)
    return response.text


def get_soup(html: str) -> bs:
    return bs(html, 'lxml')


def get_list_links(soup):
    container = soup.find('div', class_='se-news-list-page__items')
    all_news = container.find_all('div', class_='se-news-list-page__item')
    res = []
    for news in all_news:
        link = news.find('div', class_='se-material__title se-material__title--size-middle').find('a').get('href')
        res.append(link)

    return res


def get_data(link):
    html = get_html(link)
    soup = get_soup(html)
    container = soup.find('div', class_='se-material-page__body')
    title = container.find('h1', class_='se-material-page__title').text.strip()
    try:
        image = container.find('div', class_='se-photogallery-swipe__image').find('a').find('img').get('src')
    except:
        image = 'No image'
    text = container.find('div', class_='se-material-page__content').find_all('p')
    data = {'title': title, 'image': image, 'text': text}
    return data


def make_all(link):
    data = get_data(link)
    try:
        news = News.objects.create(title=data['title'], image=data['image'], text=data['text'])
    except IntegrityError as e:
        print(f"Запись с title '{data['title']}' уже существует.")
        pass


def main():
    url = get_html('https://www.sport-express.ru/news/')
    soup = get_soup(url)
    links = get_list_links(soup)
    for link in links:
        make_all(link)
    # with Pool(40) as pool:
    #     pool.map(make_all, links)


# if __name__ == '__main__':
#     main()


# class Command(BaseCommand):
#     help = 'Parsing News'
#
#     def handle(self, *args, **options):
#         url = get_html('https://www.sport-express.ru/news/')
#         soup = get_soup(url)
#         links = get_list_links(soup)
#         with Pool(40) as pool:
#             pool.map(make_all, links)

# запуск парсинга
# python manage.py parse_news