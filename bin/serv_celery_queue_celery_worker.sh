#!/bin/sh

cd ..

./manage-serv.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=queue_celery__worker \
--detach \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/queue_celery_worker.log \
--pidfile=../../run/celery__keksik_com_ua__queue_celery__worker.pid



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
