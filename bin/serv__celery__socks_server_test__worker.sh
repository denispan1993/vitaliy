#!/bin/sh

cd ..

./manage-serv.py celery worker --app=proj \
--concurrency=5 \
--autoreload \
--queues=socks_server_test \
--hostname=socks_server_test__worker \
--detach \
--loglevel=DEBUG \
--logfile=../../logs/keksik_com_ua/celery/socks_server_test__worker.log \
--pidfile=../../run/celery__keksik_com_ua__socks_server_test__worker.pid &



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
