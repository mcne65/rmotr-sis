#!/bin/bash

echo "Releasing..."

echo "====== RSYNCING LOCAL FILES ======"
rsync -avi --exclude '*__pycache__*' --exclude '*.pyc' rmotr_sis/ root@sis.rmotr.com:/opt/rmotr-sis/rmotr_sis

echo "====== COLLECTING STATIC FILES ======"
ssh root@sis.rmotr.com 'PYTHONPATH=/opt/rmotr-sis/rmotr_sis/ DJANGO_SETTINGS_MODULE=rmotr_sis.settings.production python /opt/rmotr-sis/rmotr_sis/manage.py collectstatic --noinput'

echo "====== RESTARTING APP ======"
ssh root@sis.rmotr.com 'supervisorctl restart rmotr_sis'

echo "Done."
