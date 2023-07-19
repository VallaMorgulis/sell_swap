import telebot
from telebot import types
import requests

from bs4 import BeautifulSoup as bs
from requests import get
from datetime import datetime

# API_TOKEN= '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'
# openai.api_key = API_TOKEN
TOKEN = '6323655965:AAFslqevr7HRylg4cvjxhfa1IDpwicqZwo0'
bot = telebot.TeleBot(TOKEN)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('Начнем')
keyboard.add(btn1)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Здравствуйте, я Ваш бот-консультант', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def check_answer(message):
    chat_id = message.chat.id
    if message.text == 'Начнем':
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Как оформить заказ?')
        btn2 = types.KeyboardButton('Оплата')
        btn3 = types.KeyboardButton('Сроки доставки')
        btn4 = types.KeyboardButton('Связаться с менеджером')
        btn5 = types.KeyboardButton('Стоимость доставки')
        btn6 = types.KeyboardButton('Новости спорта')
        keyboard1.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(chat_id, 'Выберите тему вопроса', reply_markup=keyboard1)

    elif message.text == 'Сроки доставки':
        bot.send_message(chat_id, f'Доставка занимает 10-12 рабочих дней')
    elif message.text == 'Как оформить заказ?':
        bot.send_message(chat_id, f'Закиньте товар в корзинку,нажмите кнопочку и товар будет оформлен')
    elif message.text == 'Стоимость доставки':
        bot.send_message(chat_id,
                         f'Доставка от 150 сом\n\nДоставка свыше 2000 сом бесплатно\n\nДоставка регионы 300 сом')
    elif message.text == 'Оплата':
        bot.send_message(chat_id, f'Наши реквизиты:\n\nОптима:4169 5577 3456 7899\n\nMBank 0700-766-345')
    elif message.text == 'Связаться с менеджером':
        bot.send_message(chat_id, f'Менеджер свяжется с вами в течение получаса. Ожидайте звонка')
    elif message.text == 'Новости спорта':
        parse_news_data(message)


def parse_news_data(message):
    chat_id = message.chat.id
    url = get_html('https://www.sport-express.ru/news/')
    soup = get_soup(url)
    container = soup.find('div', class_='se-news-list-page__items')
    all_news = container.find_all('div', class_='se-news-list-page__item')
    for news in all_news:
        title = news.find('div', class_='se-material__title se-material__title--size-middle').find('a').text
        link = news.find('div', class_='se-material__title se-material__title--size-middle').find('a').get('href')
        news = f'Новость:\n{title}\nСсылка:\n{link}'
        bot.send_message(chat_id, news)


def get_html(url: str) -> str:
    response = get(url)
    return response.text


def get_soup(html: str) -> bs:
    return bs(html, 'lxml')


# bot.polling()