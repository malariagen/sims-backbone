#!/bin/bash
set -x
INSTALL_CMD=yum
${INSTALL_CMD} install -y sudo
test -x /usr/bin/sudo && export SUDO=/usr/bin/sudo
#${SUDO} ${INSTALL_CMD} upgrade -y
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
source ~/.nvm/nvm.sh
nvm install 8
${SUDO} pip install yapf
java -version
${SUDO} ${INSTALL_CMD} install -y git python36 python36-pip libpq-dev maven openjdk-8-jdk 
${SUDO} ${INSTALL_CMD} remove -y java-1.7.0-openjdk
java -version
git clone https://github.com/malariagen/sims-backbone.git
cd sims-backbone
get checkout sqlalchemy
./generate.sh
PIP_CMD="${SUDO} /usr/bin/pip-3.6"
#${PIP_CMD} install --upgrade pip
${PIP_CMD} install -r python_client/requirements.txt
${PIP_CMD} install -r test/requirements.txt
${PIP_CMD} install -r server/backbone_server/REQUIREMENTS
${PIP_CMD} install -r upload/requirements.txt
${PIP_CMD} install git+https://github.com/idwright/chemistry-cmislib.git

cd upload
./import.sh $1
