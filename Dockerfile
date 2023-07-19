FROM python:3

ENV PYTHONIOENCODING UTF-8
ENV TZ=Asia/Bishkek

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir static && mkdir media && mkdir logs

COPY . .
#COPY telegram_bot.py /code/

EXPOSE 8000