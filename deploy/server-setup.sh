#!/usr/bin/env bash

# # Display expansions
# set -x

# # Print shell input lines as they are read
# set -v

# Exit on unset variable
set -u

# Exit on error
set -e

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

if [[ ! -v SETUP_CONFIG_DIR ]]; then
    if [[ -d /vagrant ]]; then
        SETUP_CONFIG_DIR='/vagrant/deploy'
    fi
fi

. ${SETUP_CONFIG_DIR}/setup.cfg

apt-get update


useradd -m -s /bin/bash ${OS_USER}
apt-get install -y git vim python-software-properties python-dev python-pip python3-dev
pip install virtualenv

# Maria
apt-get install software-properties-common
apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db
add-apt-repository -y 'deb [arch=amd64,i386] http://mirror.edatel.net.co/mariadb/repo/10.1/ubuntu trusty main'
apt-get update
export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< "mariadb-server-10.0 mysql-server/root_password password $MARIADB_ROOT_PASSWORD"
sudo debconf-set-selections <<< "mariadb-server-10.0 mysql-server/root_password_again password $MARIADB_ROOT_PASSWORD"
sudo apt-get install -y mariadb-server
# mysql -u$MARIADB_PASSWORD -p$MARIADB_PASSWORD -e "SET PASSWORD = PASSWORD('');"
apt-get install -y mariadb-server

su - ${OS_USER} <<EOF_su
mkdir -p $VIRTUALENV_DIR
EOF_su


su - ${OS_USER} <<EOF_su
virtualenv $VIRTUALENV_DIR/$VENV_SUPERVISOR_NAME
source $VIRTUALENV_DIR/$VENV_SUPERVISOR_NAME/bin/activate
pip install supervisor
EOF_su

su - ${OS_USER} <<EOF_su
virtualenv $VIRTUALENV_DIR/$VENV_RMOTR_SIS_NAME -p ${PYTHON_3_PATH}
source $VIRTUALENV_DIR/$VENV_RMOTR_SIS_NAME/bin/activate
EOF_su

su - ${OS_USER} <<EOF_su
cd $HOME
git clone $GIT_RMOTR_SIS_REPO

EOF_su
