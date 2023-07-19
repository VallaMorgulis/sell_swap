FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx/default.conf /etc/nginx/conf.d/

EXPOSE 80

#CMD ['nginx', '-g', 'daemon off;']
#CMD python telegram_bot.py & python manage.py runserver 0.0.0.0:8000