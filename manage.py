#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensor_tracker.configs.production")
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensor_tracker.configs.development") # use for local migration creation

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
