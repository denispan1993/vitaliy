#!/bin/sh

./manage.py \
loaddata \
apps/authModel/fixtures/Permission.initial_data.json
