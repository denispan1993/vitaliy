#!/home/user/PycharmProjects/Env/bin/python
# -*- coding: utf-8 -*-
###!/usr/www/envs/keksik_com_ua/bin/python

celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=worker1.%n \
--loglevel=DEBUG \
--logfile=bin/log/worker1.%n.log \
--pidfile=bin/pid/worker1.%n.pid



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
