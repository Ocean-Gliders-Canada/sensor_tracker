# Sensor Tracker (sensor_tracker)

Sensor tracker is a tool which includes a database, web front-end, and REST API for managing deployment, platform,
instrument, and sensor metadata. This is intended as both informational and to be used during data processing.

For license information, please refer to [**LICENSE.md**](LICENSE.md)

Setup:
=============
**Install**

* [**PostGreSQL**](https://www.postgresql.org/download/)
* [**Python 3.7**](https://www.python.org/downloads/)
* [**NGINX**](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

**Download code**

* Create ~/code/ if it does not exist `cd` into it
* `git clone git@gitlab.oceantrack.org:ocean-gliders-canada/sensor_tracker.git`
* `cd sensor_tracker`

**Setup virtualenv and create database**

* `./run.sh init`

**Run the production server**
 * Start nginx
 * `python manage.py collectstatic`
 * `uwsgi uwsgi.ini`

**Run the development server**

Debug
 * `python manage.py runserver --settings=sensor_tracker.configs.development --noreload 0.0.0.0:8010`

Run
 * Start nginx
 * `./run.sh start`

**API**

Sensor tracker has a REST API interface included. Specifications can be found at [yourdomain]/sensor_tracker/api/spec