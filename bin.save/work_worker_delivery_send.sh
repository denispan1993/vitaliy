#!/bin/sh

cd ..

./manage_workShop.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery_send \
--hostname=queues_delivery_send__worker.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_delivery_send__worker.%n.pid
