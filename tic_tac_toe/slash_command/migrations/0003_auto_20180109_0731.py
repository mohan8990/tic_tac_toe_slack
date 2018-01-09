# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-09 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slash_command', '0002_auto_20180109_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='lostBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='losses', to='slash_command.GameUser'),
        ),
        migrations.AddField(
            model_name='game',
            name='wonBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wins', to='slash_command.GameUser'),
        ),
    ]
