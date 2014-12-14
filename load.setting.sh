#!/bin/sh

./manage.py \
loaddata \
apps/utils/setting/fixtures/initial_data.json
