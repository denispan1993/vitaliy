#!/bin/sh

./manage.py \
dumpdata \
--indent 4 \
contenttypes.contenttype > apps/authModel/fixtures/Content_Type.initial_data.json
