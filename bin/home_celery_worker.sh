#!/home/user/PycharmProjects/Env/bin/python
# -*- coding: utf-8 -*-

celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=worker1.%n \
--loglevel=DEBUG \
--logfile=../logs/keksik_com_ua/celery/worker1.%n.log \
--pidfile=../run/celery__keksik_com_ua___worker1.%n.pid



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
