FROM python:3.8

RUN pip install --upgrade pip \
    && mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python /app/tBot.py