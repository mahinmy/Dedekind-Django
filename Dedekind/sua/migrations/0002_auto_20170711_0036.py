# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-10 16:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sua', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sua',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sua',
            name='sua_hours',
            field=models.FloatField(),
        ),
    ]