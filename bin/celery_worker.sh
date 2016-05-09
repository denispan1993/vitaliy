#!/usr/www/envs/keksik_com_ua/bin/python

python celery worker --app proj --detach \
--concurrency=1 \
--autoreload \
--hostname worker1.%h \
--loglevel DEBUG \
--logfile /usr/www/logs/keksik_com_ua/celery_worker1.%n.log \
--pidfile=/var/run/celery/worker1.%n.pid



# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.

