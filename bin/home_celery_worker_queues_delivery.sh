#!/bin/sh

cd ..

#./manage_ubuntuhome.py celery worker --app=proj \

./manage_tor.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=delivery \
--hostname=queues_delivery__worker1.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua__queues_delivery__worker1.%n.pid

#--logfile=../logs/keksik_com_ua/celery/worker1.%n.log \


# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.