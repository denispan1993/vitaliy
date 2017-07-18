#!/bin/sh

cd ..

./../../PyEnv/versions/3.6.1/envs/keksik/bin/celery worker --beat \
--app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=queues_celery__worker.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_celery__worker.%n.pid
