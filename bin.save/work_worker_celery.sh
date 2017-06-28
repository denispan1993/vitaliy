#!/bin/sh

cd ..

./manage_workShop.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=queues_celery__worker.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_celery__worker.%n.pid
