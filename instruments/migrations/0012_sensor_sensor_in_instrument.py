# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-06-19 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('instruments', '0011_auto_20190619_1703'),
    ]

    operations = [
        migrations.RunSQL(
            "update instruments_sensor set created_date = modified_date where created_date is null;"
        ),
        migrations.RunSQL(
            """
with e as (
    SELECT
      id,
      created_date,
      (
        SELECT p2.created_date
        FROM instruments_sensor p2
        WHERE p2.created_date IS NOT NULL AND p2.id <= p1.id
        ORDER BY p2.id DESC
        LIMIT 1
      ) AS new_value
    FROM instruments_sensor p1
    ORDER BY id
)
update instruments_sensor
set created_date = e.new_value
from e
where instruments_sensor.id = e.id and instruments_sensor.created_date is null;
"""
        ),
        migrations.RunSQL(
            """with e2 as (
    SELECT
      id,
      created_date,
      (
        SELECT p2.created_date
        FROM instruments_sensor p2
        WHERE p2.created_date IS NOT NULL AND p2.id >= p1.id
        ORDER BY p2.id asc
        LIMIT 1
      ) AS new_value
    FROM instruments_sensor p1
    ORDER BY id
)
update instruments_sensor
set created_date = e2.new_value
from e2
where instruments_sensor.id = e2.id and instruments_sensor.created_date is null;

"""
        ),
        migrations.RunSQL(
            "insert into instruments_sensoroninstrument(instrument_id, sensor_id,start_time) select s.instrument_id, s.id, s.created_date from instruments_sensor as s;"
        ),
    ]
