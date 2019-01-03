#!/bin/bash
set -x
INSTALL_CMD=yum
${INSTALL_CMD} install -y sudo
test -x /usr/bin/sudo && export SUDO=/usr/bin/sudo
#${SUDO} ${INSTALL_CMD} upgrade -y
${SUDO} ${INSTALL_CMD} install -y git python36 python36-pip
git clone https://github.com/malariagen/sims-backbone.git
cd sims-backbone
./generate.sh
PIP_CMD="${SUDO} /usr/bin/pip-3.6"
#${PIP_CMD} install --upgrade pip
${PIP_CMD} install -r python_client/requirements.txt
${PIP_CMD} install -r test/requirements.txt
${PIP_CMD} install -r server/backbone_server/REQUIREMENTS
${PIP_CMD} install -r upload/requirements.txt
${PIP_CMD} install git+https://github.com/idwright/chemistry-cmislib.git

cd upload
./import.sh
