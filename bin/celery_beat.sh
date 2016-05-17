#!/home/user/PycharmProjects/Env/bin/python
# -*- coding: utf-8 -*-
###!/usr/www/envs/keksik_com_ua/bin/python

celery beat --app=proj \
--scheduler=djcelery.schedulers.DatabaseScheduler \
--loglevel=DEBUG \
--logfile=bin/log/beat.log \
--pidfile=bin/pid/beat.pid
