#!/bin/sh

cd ..

./manage-serv.py celery beat --app=proj \
--scheduler='djcelery.schedulers.DatabaseScheduler' \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/beat.log \
--pidfile=../../run/celery__keksik_com_ua__beat.pid
