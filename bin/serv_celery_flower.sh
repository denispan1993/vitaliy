#!/bin/sh

cd ..

celery flower --app=proj \
--address=192.168.1.99 \
--port=5555 \
--broker=django://localhost//
