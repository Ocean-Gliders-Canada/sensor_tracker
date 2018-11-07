# Sensor Tracker (sensor_tracker)

Sensor tracker is a tool which includes a database, web front-end, and REST API for managing deployment, platform,
instrument, and sensor metadata. This is intended as both informational and to be used during data processing.

For license information, please refer to [**LICENSE.md**](LICENSE.md)

Setup:
=============
**Install**

* [**PostGreSQL**](https://www.postgresql.org/download/)
* [**Python 2.7**](https://www.python.org/downloads/)
* [**NGINX**](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

**Download code**

* Create a folder to hold repository code, `cd` into it
* `git clone git@gitlab.oceantrack.org:ocean-gliders-canada/sensor_tracker.git`
* `cd sensor_tracker`

**Setup virtualenv**

* `pip install virtualenv`
* `mkdir venv`
* `virtualenv -p /path/to/python2.7 venv`
* `source venv/bin/activate`
* `pip install -r ~/code/sensor_tracker/requirements.txt`

**Create sensor_tracker database**

* Open psql shell
* `CREATE ROLE sensor_tracker WITH LOGIN PASSWORD 'yourpass';`
* `ALTER ROLE sensor_tracker CREATEDB;`
* `CREATE DATABASE sensor_tracker;`
* Close psql shell
* `python manage.py migrate`
* `python manage.py createsuperuser`
* In settings/development.py, edit the DATABASES object to include the username and password used to create your database.

**Run the production server**

 * `python manage.py collectstatic`
 * Start nginx
 * `uwsgi uwsgi.ini`

**Run the development server**

* `python manage.py runserver --settings=sensor_tracker.configs.development --noreload 0.0.0.0:8000`

**API**

Sensor tracker has a REST API interface included. Specifications can be found at [yourdomain]/sensor_tracker/api/spec