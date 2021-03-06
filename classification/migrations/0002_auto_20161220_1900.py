# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name_plural': 'repositories'},
        ),
        migrations.AlterField(
            model_name='repository',
            name='category',
            field=models.CharField(blank=True, choices=[('DEV', 'DEV'), ('HW', 'HW'), ('EDU', 'EDU'), ('DOCS', 'DOCS'), ('WEB', 'WEB'), ('DATA', 'DATA'), ('OTHER', 'OTHER')], max_length=10),
        ),
        migrations.AlterField(
            model_name='repository',
            name='url',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
