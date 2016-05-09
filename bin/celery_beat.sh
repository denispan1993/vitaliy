#!/usr/www/envs/keksik_com_ua/bin/python

python celery beat --app proj --detach \
--loglevel DEBUG \
--logfile /usr/www/logs/keksik_com_ua/celery_beat.%n.log \
--pidfile=/var/run/celery/beat.%n.pid
