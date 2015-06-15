#!/bin/bash

echo "Releasing..."

echo "Backing up database"
ssh root@sis.rmotr.com 'PYTHONPATH=/opt/rmotr-sis/rmotr_sis/ DJANGO_SETTINGS_MODULE=rmotr_sis.settings.production python /opt/rmotr-sis/rmotr_sis/manage.py dbbackup'
ssh root@sis.rmotr.com 'mv /root/default.backup /home/mzugnoni/rmotr_sis_$(date +%F-%H:%M:%S).sql'

echo "====== RSYNCING LOCAL FILES ======"
rsync -ai --exclude '*__pycache__*' --exclude '*.pyc' rmotr_sis/ root@sis.rmotr.com:/opt/rmotr-sis/rmotr_sis
rsync -ai requirements/ root@sis.rmotr.com:/opt/rmotr-sis/requirement
rsync -ai static/ root@sis.rmotr.com:/opt/rmotr-sis/static

echo "====== COLLECTING STATIC FILES ======"
ssh root@sis.rmotr.com 'PYTHONPATH=/opt/rmotr-sis/rmotr_sis/ DJANGO_SETTINGS_MODULE=rmotr_sis.settings.production python /opt/rmotr-sis/rmotr_sis/manage.py collectstatic --noinput'

echo "====== INSTALLING DEPENDENCIES ======"
ssh root@sis.rmotr.com 'pip install -r /opt/rmotr-sis/requirements/base.txt'

echo "====== MIGRATING DATABASE ======"
ssh root@sis.rmotr.com 'PYTHONPATH=/opt/rmotr-sis/rmotr_sis/ DJANGO_SETTINGS_MODULE=rmotr_sis.settings.production python /opt/rmotr-sis/rmotr_sis/manage.py migrate'

echo "====== RESTARTING APP ======"
ssh root@sis.rmotr.com 'supervisorctl restart rmotr_sis'

echo "Done."
