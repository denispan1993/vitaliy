#!/bin/sh

cd ..

./manage-serv.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=worker \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/worker.log \
--pidfile=../../run/celery__keksik_com_ua__worker.pid



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
