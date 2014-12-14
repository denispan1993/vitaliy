#!/bin/sh

./serv-manage.py \
dumpdata \
--indent 4 \
contenttypes.contenttype > apps/authModel/fixtures/ContentType.initial_data.json
