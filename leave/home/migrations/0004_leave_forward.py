# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20170830_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='forward',
            field=models.IntegerField(default='0'),
        ),
    ]
