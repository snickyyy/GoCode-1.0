FROM python:3.12-alpine

RUN apk update

RUN python -m pip install --upgrade pip && pip install redis

WORKDIR /GoCode

CMD ["/bin/sh"]