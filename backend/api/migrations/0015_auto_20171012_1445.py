# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 18:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20171012_1445'),
        ('api', '0014_auto_20171011_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
