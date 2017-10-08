#!/bin/sh

cd ..

./../../PyEnv/versions/3.6.1/envs/keksik/bin/celery worker \
--beat \
--app=proj \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__beat.%n.pid
