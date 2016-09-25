#!/bin/sh

cd ..

./manage-serv.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=queues__socks_server_get \
--hostname=queues__socks_server_get__worker \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/queues__socks_server_get__worker.log \
--pidfile=../../run/celery__keksik_com_ua__queue_socks_server_get__worker.pid &

#--detach \


# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
