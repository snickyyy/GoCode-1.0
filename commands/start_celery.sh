#!/bin/sh

cd /GoCode/src && celery -A config worker --loglevel=${CELERY_LOG_LEVEL} -c ${CELERY_WORKERS_NUMBER} & cd /GoCode/src && celery -A config flower --broker=redis://redis