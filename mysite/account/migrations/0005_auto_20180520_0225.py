# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-05-20 02:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_usertest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertest',
            name='test',
        ),
        migrations.DeleteModel(
            name='UserTest',
        ),
    ]