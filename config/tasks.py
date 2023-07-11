from django.core.mail import send_mail

from account.send_mail import send_notification
# from comment.models import Comment
from .celery import app


@app.task
def send_notification_task(user_email, order_id, price):
    send_notification(user_email, order_id, price)

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