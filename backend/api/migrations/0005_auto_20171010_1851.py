# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_product_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cover',
            field=models.ImageField(default='images/no_image.gif', upload_to='images/'),
        ),
    ]