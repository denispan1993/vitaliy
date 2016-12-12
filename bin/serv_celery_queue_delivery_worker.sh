#!/bin/sh

cd /www/projs/keksik_com_ua/

./manage-serv.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery \
--hostname=queue_delivery \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/queue_delivery.log \
--pidfile=../../run/celery__keksik_com_ua__queue_delivery.pid &



#--detach \

# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
