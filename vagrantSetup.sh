#!/bin/bash

# Script to install and initialize Web Rekollect

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3-pip git postgresql libncurses5-dev -y
cd rekollect
sudo pip3 install --upgrade pip
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install --editable .
git clone https://github.com/google/rekall-profiles.git
sudo -u postgres createuser -s ubuntu -w
createdb rekollect
