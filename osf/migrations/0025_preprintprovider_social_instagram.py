# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-09 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0024_auto_20161209_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='preprintprovider',
            name='social_instagram',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]