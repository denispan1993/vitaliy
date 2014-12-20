#!/bin/sh

./manage.py \
loaddata \
apps/authModel/fixtures/ContentType.initial_data.json
