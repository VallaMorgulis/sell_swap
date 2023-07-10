import os

from django.core.mail import send_mail

HOST = 'localhost:8000'


def send_confirmation_email(user, code):
    # link = f'http://{os.environ.get("HOST")}' \
    #        f'/api/v1/account/activate/{code}'
    link = f'http://{HOST}/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке ниже:'
        f'\n{link}'
        f'\nСсылка работает один раз!',
        'kochemarov@gmail.com',
        [user],
        fail_silently=False,
    )
