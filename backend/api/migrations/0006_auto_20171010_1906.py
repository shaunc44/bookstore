# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20171010_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cover',
            field=models.ImageField(default='static/images/no_image.gif', upload_to='static/images/'),
        ),
    ]
