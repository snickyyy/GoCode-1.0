#!/bin/sh

cd /GoCode/src && celery -A config flower --broker=redis://redis