#!/www/envs/keksik_com_ua/bin/python
# -*- coding: utf-8 -*-

celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=worker1.%n \
--loglevel=DEBUG \
--logfile=../logs/keksik_com_ua/celery/worker1.%n.log \
--pidfile=../../run/celery__keksik_com_ua__worker1.%n.pid



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
