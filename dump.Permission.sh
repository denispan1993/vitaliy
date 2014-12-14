#!/bin/sh

./manage.py \
dumpdata \
--indent 4 \
auth.Permission > apps/authModel/fixtures/Permission.initial_data.json.save
