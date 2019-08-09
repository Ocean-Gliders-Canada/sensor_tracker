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

**Setup**

* Refer to run.sh for most setup operations 
* Setup virtualenv and create database locally
  * `./run.sh dev init`
* Run server locally
  * `./run.sh dev start`
* Debug in PyCharm: 
  * Additional options: --settings=sensor_tracker.configs.development --noreload
  * Port: 8010
  * Python interpreter: ~/code/sensor_tracker/venv/bin/python

**API**

Sensor tracker has a REST API interface included. Specifications can be found at [yourdomain]/sensor_tracker/api/spec