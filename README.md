# rmotr-sis
Student information system for rmotr.com organization.

### Installation

```bash
$ git clone https://github.com/rmotr/rmotr-sis.git
$ cd rmotr-sis
$ mkvirtualenv rmotr-sis -a .
$ pip install -r requirements/dev.txt
$ echo "export DJANGO_SETTINGS_MODULE=rmotr_sis.settings.dev" >> ${HOME}/.virtualenvs/rmotr-sis/bin/postactivate
$ echo "unset DJANGO_SETTINGS_MODULE" >> ${HOME}/.virtualenvs/rmotr-sis/bin/postdeactivate
```

### Usage

```bash
$ cd /rmotr_sis
$ python manage.py syncdb
$ python manage.py runserver
```

Have fun!
