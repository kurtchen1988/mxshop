# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-07 22:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0005_auto_20190107_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='signer_modile',
            new_name='signer_mobile',
        ),
    ]
