.PHONY: backup-production-db rsync-local-files collect-static install-dependencies migrate-database restart-app deploy

TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"
DATE=`date +%F-%H:%M:%S`

USER=root
HOST=sis.rmotr.com
SSH_CONN=$(USER)@$(HOST)
PROJECT_ROOT=/opt/rmotr-sis

PYTHONPATH=/opt/rmotr-sis/rmotr_sis/
DJANGO_SETTINGS_MODULE=rmotr_sis.settings.production

MANAGE_COMMAND=/opt/rmotr-sis/rmotr_sis/manage.py

SIS_COMMAND="PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) python $(MANAGE_COMMAND) "

backup-production-db:
		@echo $(TAG)Backing up production database $(END)
		ssh $(SSH_CONN) $(SIS_COMMAND) dbbackup
		ssh $(SSH_CONN) "mv /root/default.backup /home/mzugnoni/backups/rmotr_sis_$(DATE).sql"

rsync-local-files:
		@echo $(TAG)Rsyncing local files$(END)
		rsync -ai --exclude '*__pycache__*' --exclude '*.pyc' rmotr_sis/ $(SSH_CONN):$(PROJECT_ROOT)/rmotr_sis
		rsync -ai requirements/ $(SSH_CONN):$(PROJECT_ROOT)/requirements
		rsync -ai static/ $(SSH_CONN):$(PROJECT_ROOT)/static
		rsync -ai .git/ $(SSH_CONN):$(PROJECT_ROOT)/.git

collect-static:
		@echo $(TAG)Collecting static files$(END)
		ssh $(SSH_CONN) $(SIS_COMMAND) collectstatic --noinput

install-dependencies:
		@echo $(TAG)Installing requirements$(END)
		ssh $(SSH_CONN) 'pip install -r /opt/rmotr-sis/requirements/base.txt'

migrate-database:
		@echo $(TAG)Applying migrations$(END)
		ssh $(SSH_CONN) $(SIS_COMMAND) migrate

restart-app:
		@echo $(TAG)Restarting app$(END)
		ssh $(SSH_CONN) 'supervisorctl restart rmotr_sis'

deploy: backup-production-db rsync-local-files install-dependencies collect-static migrate-database restart-app
		@echo $(TAG)Done.$(END)


PROJECT_DIR=$(HOME)/rmotr-sis
VIRTUALENVS_DIR=$(HOME)/virtualenvs

SUPERVISORD_PID=/tmp/supervisord.pid
SUPERVISORD_PATH=$(VIRTUALENVS_DIR)/supervisord/bin/supervisord
SUPERVISORCTL_PATH=$(VIRTUALENVS_DIR)/supervisord/bin/supervisorctl
SUPERVISORD_CONF=$(PROJECT_DIR)/deploy/conf/supervisord.conf

supervisor-start:
		 $(SUPERVISORD_PATH) -c $(SUPERVISORD_CONF)

supervisor-status:
		$(SUPERVISORCTL_PATH) -c $(SUPERVISORD_CONF) status

supervisor-reload:
		kill -s HUP `cat $(SUPERVISORD_PID)`

supervisor-stop:
		kill -2 `cat $(SUPERVISORD_PID)`

rmotr-sis-stop:
		$(SUPERVISORCTL_PATH) -c $(SUPERVISORD_CONF) stop $(FEED_API_PROCCESS_NAME)

rmotr-sis-start:
		$(SUPERVISORCTL_PATH) -c $(SUPERVISORD_CONF) start $(FEED_API_PROCCESS_NAME)

rmotr-sis-reload:
		$(SUPERVISORCTL_PATH) -c $(SUPERVISORD_CONF) reload $(FEED_API_PROCCESS_NAME)
