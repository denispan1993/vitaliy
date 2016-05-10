#!/home/user/PycharmProjects/Env/bin/python
# -*- coding: utf-8 -*-
###!/usr/www/envs/keksik_com_ua/bin/python

celery beat -A proj \
--loglevel DEBUG \
--logfile /usr/www/logs/keksik_com_ua/celery_beat.%n.log \
--pidfile=bin/beat.%n.pid
