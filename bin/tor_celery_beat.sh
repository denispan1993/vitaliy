#!/bin/sh

cd ..

./manage_tor.py celery beat --app=proj \
--scheduler=djcelery.schedulers.DatabaseScheduler \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__beat.pid
