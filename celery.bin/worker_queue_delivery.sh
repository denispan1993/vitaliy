#!/bin/sh

cd ..

# ./../../PyEnv/versions/3.6.1/envs/keksik/bin/celery worker \
./../../PyEnv/versions/shop/bin/celery worker \
--app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery \
--hostname=worker__queues__delivery.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__worker__queues__delivery.%n.pid
