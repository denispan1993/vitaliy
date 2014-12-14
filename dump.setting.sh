#!/bin/sh

./manage.py \
dumpdata \
--indent 4 \
setting > apps/utils/setting/fixtures/initial_data.json
