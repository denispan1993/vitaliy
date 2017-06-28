#!/bin/sh

cd ..

./manage_ubuntuhome.py celery worker --app=proj \
--concurrency=50 \
--autoreload \
--queues=socks_server_test \
--hostname=queues_socks_server_test__worker.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_socks_server_test__worker.%n.pid
