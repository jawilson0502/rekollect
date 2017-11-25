# Rekollect: Web App for Rekall

Rekollect is an open source  web application for the [Rekall Memory Forensics Framework](https://rekall-forensic.com)

This has been tested with Debian 9 and Ubuntu 16.04 LTS with Python 3

## Install Instructions
Rekollect requires Python 3 and is best run in a virtual environment. Rekollect also requires rekall-profiles to be downloaded locally to be referenced. Make sure to edit your `rekollect/web_rekollect/config.yaml` to be appropriate from your environment. Postgresql will also need to be configured to allow password logins.

Dependencies:
```
$ sudo apt-get install git libncurses5-dev postgresql python3-pip
```
Instructions:
```
$ git clone https://github.com/jawilson0502/rekollect.git
$ cd rekollect
$ git clone https://github.com/google/rekall-profiles.git
$ sudo pip3 install --upgrade pip
$ sudo pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install --editable .
$ cd web_rekollect
$ sudo -u postgres createuser -d <username> -W
$ createdb rekollect
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ export FLASK_APP="web_rekollect"
$ flask run
```
You can now connect to your instance at `127.0.0.1:5000`

## Plugins supported
* imageinfo
* pslist
* connscan / netscan
* filescan
* shimcachemem

## Future plans
* Get a Vagrantfile to spin up a quick dev environment
* Expand the number of plugins supported. Next planned plugins are:
  * dumpfiles
  * ldrmodules
  * dlllist
  * vad
  * printkey
  * and more based on suggestions (create an issue to request a particular plugin)
