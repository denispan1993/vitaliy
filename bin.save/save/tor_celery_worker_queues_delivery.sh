#!/bin/sh

cd ..

./manage_tor.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery \
--hostname=queues_delivery__worker1.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_delivery__worker.%n.pid
