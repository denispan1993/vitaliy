#!/bin/sh

cd /www/projs/keksik_com_ua/

./manage-serv.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=queue_celery \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/queue_celery.log \
--pidfile=../../run/celery__keksik_com_ua__queue_celery.pid



#--detach \

# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
