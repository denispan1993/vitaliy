#!/bin/sh

./manage.py \
dumpdata \
--indent 4 \
authModel > apps/authModel/fixtures/initial_data.json
