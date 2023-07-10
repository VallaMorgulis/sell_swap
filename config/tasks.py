from django.core.mail import send_mail

from account.send_mail import send_confirmation_email
from .celery import app


@app.task
def send_confirmation_email_task(user, code):
    send_confirmation_email(user, code)


@app.task
def send_notification_task(user, order_id, price):
    send_mail(
        'Уведомление о создании заказа!',
        f'''Вы создали заказ №{order_id}, ожидайте звонка!
            Полная стоимость вашего заказа: {price}.
            Спасибо за то что выбрали нас!''',
        'from@exmple.com',
        [user],
        fail_silently=False
    )

# @app.task
# def send_comment_notification_email(comment_id):
#     # Получите комментарий по его ID или каким-либо другим способом
#     comment = Comment.objects.get(id=comment_id)
#
#     # Отправьте уведомление о комментарии по электронной почте
#     subject = 'Уведомление о новом комментарии'
#     message = f'Получен новый комментарий от пользователя {comment.user}: {comment.content}'
#     recipient_list = [comment.user.email]
#     send_mail(subject, message, 'noreply@example.com', recipient_list, fail_silently=False)
