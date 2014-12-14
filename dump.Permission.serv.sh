#!/bin/sh

./serv-manage.py \
dumpdata \
--indent 4 \
auth.Permission > apps/authModel/fixtures/Permission.initial_data.json
