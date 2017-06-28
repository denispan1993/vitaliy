#!/bin/sh

cd ..

./manage_ubuntuhome.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=socks_server_get \
--hostname=queues_socks_server_get__worker.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_socks_server_get__worker.%n.pid
