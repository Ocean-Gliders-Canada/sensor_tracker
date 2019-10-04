#!/bin/bash

PROJECT=sensor_tracker
SETTINGS_PARENT=sensor_tracker.configs.
PENV_TYPE=conda

if [[ ! -d ~/code/deploy_tools ]]; then
    echo "Missing ceotr-public/deploy_tools repo, clone to ~/code first"
    exit 1
fi
source ~/code/deploy_tools/run_common.sh

DB_NAME="sensor_tracker"
UWSGI_CONFIG="$REPO/uwsgi.ini"
DB_ROLE=sensor_tracker

init()
{
    init_py_env
    init_database
}

status()
{
    if [[ "$(pgrep -f "$UWSGI_CONFIG")" != "" ]]; then
        echo "-  web server status: Running"
        return 0
    else
        echo "-  web server status: Not running"
        return 1
    fi
}

stop()
{
    if status; then
        echo "-> Stopping django server"
        pgrep -f "$UWSGI_CONFIG" | xargs kill -9
    fi
}

update()
{
    backup_database
    update_code
    update_py_env
    migrate_database
}

start()
{
    start_nginx
    if ! status; then
        echo "-> Starting django server"
        LOG_FILE="${LOGS}/server.$(date "+%Y_%m_%d").log"
        nohup uwsgi ${UWSGI_CONFIG} >> ${LOG_FILE} 2>&1 &
        sleep 5
        echo -e "tail -n 200 ${LOG_FILE}\n======================="
        tail -n 200 ${LOG_FILE}
    fi
}

show_help()
{
    echo "Available commands and sub-commands:"
    echo "    init (install_virtualenv, init_py_env, init_database)"
    echo "    status"
    echo "    stop"
    echo "    update (backup_database, update_code, update_py_env, migrate_database)"
    echo "    start"
    show_common_help
}


execute "$@"
