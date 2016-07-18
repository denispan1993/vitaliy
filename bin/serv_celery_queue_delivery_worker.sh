#!/bin/sh

cd ..

./manage-serv.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery \
--hostname=queue_delivery__worker \
--detach \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/queue_delivery_worker.log \
--pidfile=../../run/celery__keksik_com_ua__queue_delivery__worker.pid &



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
