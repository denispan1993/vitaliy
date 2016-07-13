#!/bin/sh

/bin/cat /www/run/celery__keksik_com_ua__queue_delivery__worker.pid | /usr/bin/xargs /bin/kill -9
