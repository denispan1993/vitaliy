#!/bin/sh

cd /www/projs/keksik_com_ua/

./manage-serv.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery_send \
--hostname=queue_delivery_send \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/queue_delivery_send.log \
--pidfile=../../run/celery__keksik_com_ua__queue_delivery_send.pid &



#--detach \

# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
