#!/bin/bash
cd `dirname $0`/..
source ../venv3/bin/activate
python manage.py prescriu_incidencies
