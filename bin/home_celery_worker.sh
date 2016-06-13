#!/bin/sh

cd ..

#./manage_ubuntuhome.py celery worker --app=proj \

./manage_tor.py celery worker --app=proj \
--concurrency=1 \
--autoreload \
--queues=celery \
--hostname=worker1.%n \
--loglevel=DEBUG \
--pidfile=../run/celery__keksik_com_ua___worker1.%n.pid

#--logfile=../logs/keksik_com_ua/celery/worker1.%n.log \


# %h: Hostname including domain name.
# %n: Hostname only.
# %d: Domain name only.
