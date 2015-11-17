# rmotr-sis
Student information system for rmotr.com organization.

### Requirements

- virtualenvwrapper

### Installation

```bash
$ git clone https://github.com/rmotr/rmotr-sis.git
$ cd rmotr-sis
$ mkvirtualenv rmotr-sis -a .
$ pip install -r requirements/dev.txt
$ echo "export DJANGO_SETTINGS_MODULE=rmotr_sis.settings.dev" >> ${HOME}/.virtualenvs/rmotr-sis/bin/postactivate
$ echo "unset DJANGO_SETTINGS_MODULE" >> ${HOME}/.virtualenvs/rmotr-sis/bin/postdeactivate
```

### Static

You need to have bower installed.
```bash
$ npm install -g bower
$ bower install
```


### Usage

```bash
$ cd /rmotr_sis
$ python manage.py syncdb
$ python manage.py runserver
```

### Development

We keep track of the pending chores with Github's [issue tracker](https://github.com/rmotr/rmotr-sis/issues). Every issue is orgaized with a set of labels.

#### Priority (required)
In order to organize the work priorities we should mark every issue with either:
 * `prt-high`: The issue must be resolved as soon as possible.
 * `prt-normal`: The issue will be assigned in next sprint.
 * `prt-low`: Issue is low level.

#### Status (required)

 * `st-new`: no one has started it
 * `st-in-progress`: someone has started it. You shouldn't tackle it. You might provide comments or ping the dev in charge if you don't see progress.
 * `st-delivered`: The issue is finished and it's pending review by the issue requester. When you finish an issue make sure you mark it as `st-delivered` and mention the creator in the comments.

#### Feature (optional)
There are parts of the system that are broad enough to have their own label. Examples:

 * `ft-assigments`
 * `ft-applications`

### Getting things done with issues

High priority issues: [https://github.com/rmotr/rmotr-sis/labels/prt-high](https://github.com/rmotr/rmotr-sis/labels/prt-high)

Have fun!
