FROM python:3.7-alpine3.8

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app

RUN apk --no-cache add libxslt \
  && apk --no-cache add --virtual .build-deps \
    build-base libxml2-dev libxslt-dev \
  && pip install -r requirements.txt \
  && apk del .build-deps

COPY . /usr/src/app
