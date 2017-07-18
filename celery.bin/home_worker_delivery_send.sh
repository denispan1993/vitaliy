#!/bin/sh

cd ..

./../../PyEnv/versions/3.6.1/envs/keksik/bin/celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery_send \
--hostname=queues_delivery_send__worker.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_delivery_send__worker.%n.pid
