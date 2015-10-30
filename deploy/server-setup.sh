#!/usr/bin/env bash

# Display expansions
set -x

# Print shell input lines as they are read
set -v

# Exit on unset variable
set -u

# Exit on error
set -e

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

. /setup.cfg

useradd -m -s /bin/bash ${OS_USER}


su - ${OS_USER} <<EOF_su
$VIRTUALENV_DIR=$HOME/virtualens

mkdir -p $VIRTUALENV_DIR

cd $HOME/virtualenv
virtualenv supervisor_env
source $HOME/virtualenv/supervisor_env/bin/activate
pip install supervisor
cd /vagrant/web_api/feed-api/
make supervisor-start
EOF_su
