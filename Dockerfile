FROM python:3.12-alpine

RUN apk update
RUN mkdir /GoCode
RUN apk add --no-cache docker-cli

WORKDIR /GoCode

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

COPY ./commands ./commands

RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt

CMD ["/bin/sh"]