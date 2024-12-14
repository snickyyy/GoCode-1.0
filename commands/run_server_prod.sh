#!/bin/sh

python ./src/manage.py collectstatic --noinput

python src/manage.py makemigrations
python src/manage.py migrate

gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir ./src config.wsgi:application --log-level=${WSGI_LOG_LEVEL}
