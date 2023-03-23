FROM python:3.9-slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Daniyal Issin <dany121822@gmail.com>" \
      version="1.0"

CMD app.py