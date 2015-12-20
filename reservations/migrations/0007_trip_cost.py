# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_trip_public_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]