#!/home/user/PycharmProjects/Env/bin/python
# -*- coding: utf-8 -*-
###!/usr/www/envs/keksik_com_ua/bin/python

python ./manage_ubuntuhome.py celery worker --app proj \
--concurrency=1 \
--autoreload \
--hostname worker1.%h \
--loglevel DEBUG \
--logfile /usr/www/logs/keksik_com_ua/celery_worker1.%n.log \
--pidfile=bin/worker1.%n.pid



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.

