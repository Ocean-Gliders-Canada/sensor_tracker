#!/bin/bash

PROJECT=sensor_tracker

. app_common/deploy/run_common.sh

DB_NAME="sensor_tracker$SUFFIX"
UWSGI_CONFIG="$REPO/uwsgi$SUFFIX.ini"

init()
{
    install_virtualenv
    init_venv
    init_database
}

init_database()
{
    if [[ "$(psql -h localhost -U sensor_tracker -c "SELECT datname FROM pg_catalog.pg_database WHERE datname = 'sensor_tracker';" postgres | grep "1 row")" -eq "" ]]; then
        psql -c "CREATE ROLE sensor_tracker WITH LOGIN PASSWORD '12345';"
        psql -c "ALTER ROLE sensor_trackerCREATEDB;"
        psql -c "CREATE DATABASE sensor_tracker$SUFFIX;"
        python manage.py migrate
        python manage.py createsuperuser
    fi
}

status()
{
    if [[ "$(pgrep -f "$UWSGI_CONFIG")" != "" ]]; then
        echo "- web server status: Running"
        return 0
    else
        echo "- web server status: Not running"
        return 1
    fi
}

stop()
{
    if status; then
        echo "-> Stopping django server"
        pgrep -f "$UWSGI_CONFIG" | sudo xargs kill -9
    fi
}

update()
{
    backup_database
    update_code
    update_venv
    update_database
}

backup_database()
{
    if [[ ! -d "$DB_BACKUPS" ]]; then
      mkdir "$DB_BACKUPS"
    fi

    PATH="$DB_BACKUPS/$ENV_$(date +"%Y_%m_%d").dump"

    /usr/bin/pg_dump -U sensor_tracker $DB_NAME > $PATH

    if [[ $? -eq 0 ]]; then
        echo "Backup created at $PATH"
    else
        echo "Failed to backup database"
    fi
}

load_database()
{
    echo "!!!load_database not yet implemented!!!"
    exit 1
}

update_venv()
{
    source venv/bin/activate
    pip install -r $REPO/requirements.txt
}

update_database()
{
    $VENV/bin/python $REPO/manage.py migrate
}

start()
{
    if ! status; then
        echo "-> Starting django server"
        gzip $LOGS/*.log
        nohup uwsgi $REPO/uwsgi.ini >> "$LOGS/server.$(date "+%Y_%m_%d_%I_%M_%p").log" 2>&1 &
    fi
}

show_help()
{
    echo "Available commands and sub-commands:"
    echo "    init (install_virtualenv, init_venv, init_database)"
    echo "    status"
    echo "    stop"
    echo "    update (backup_database, update_code, update_environment, update_database)"
    echo "    start"
    echo "    load_database"
    show_common_help
}


execute $1 $2
